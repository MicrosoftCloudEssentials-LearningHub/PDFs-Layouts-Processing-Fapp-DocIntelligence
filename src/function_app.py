import logging
import azure.functions as func
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential
import os
import uuid
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

## DEFINITIONS 
def initialize_form_recognizer_client():
    endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("FORM_RECOGNIZER_KEY")
    if not isinstance(key, str):
        raise ValueError("FORM_RECOGNIZER_KEY must be a string")
    logging.info(f"Form Recognizer endpoint: {endpoint}")
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def read_pdf_content(myblob):
    logging.info(f"Reading PDF content from blob: {myblob.name}")
    return myblob.read()

def analyze_pdf(form_recognizer_client, pdf_bytes):
    logging.info("Starting PDF layout analysis.")
    poller = form_recognizer_client.begin_analyze_document(
        model_id="prebuilt-layout",
        document=pdf_bytes
    )
    logging.info("PDF layout analysis in progress.")
    result = poller.result()
    logging.info("PDF layout analysis completed.")
    logging.info(f"Document has {len(result.pages)} page(s), {len(result.tables)} table(s), and {len(result.styles)} style(s).")
    return result

def extract_layout_data(result):
    logging.info("Extracting layout data from analysis result.")

    layout_data = {
        "id": str(uuid.uuid4()),
        "pages": []
    }

    # Log styles
    for idx, style in enumerate(result.styles):
        content_type = "handwritten" if style.is_handwritten else "no handwritten"
        logging.info(f"Document contains {content_type} content")

    # Process each page
    for page in result.pages:
        logging.info(f"--- Page {page.page_number} ---")
        page_data = {
            "page_number": page.page_number,
            "lines": [line.content for line in page.lines],
            "tables": [],
            "selection_marks": [
                {"state": mark.state, "confidence": mark.confidence}
                for mark in page.selection_marks
            ]
        }

        # Log extracted lines
        for line_idx, line in enumerate(page.lines):
            logging.info(f"Line {line_idx}: '{line.content}'")

        # Log selection marks
        for selection_mark in page.selection_marks:
            logging.info(
                f"Selection mark is '{selection_mark.state}' with confidence {selection_mark.confidence}"
            )

        # Extract tables
        page_tables = [
            table for table in result.tables
            if any(region.page_number == page.page_number for region in table.bounding_regions)
        ]

        for table_index, table in enumerate(page_tables):
            logging.info(f"Table {table_index}: {table.row_count} rows, {table.column_count} columns")

            table_data = {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": []
            }

            for cell in table.cells:
                content = cell.content.strip()
                table_data["cells"].append({
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "content": content
                })
                logging.info(f"Cell[{cell.row_index}][{cell.column_index}]: '{content}'")

            page_data["tables"].append(table_data)

        layout_data["pages"].append(page_data)

    try:
        preview = json.dumps(layout_data, indent=2)
        logging.info("Structured layout data preview:\n" + preview)
    except Exception as e:
        logging.warning(f"Could not serialize layout data for preview: {e}")

    return layout_data

def save_layout_data_to_cosmos(layout_data):
    try:
        endpoint = os.getenv("COSMOS_DB_ENDPOINT")
        key = os.getenv("COSMOS_DB_KEY")
        aad_credentials = DefaultAzureCredential()
        client = CosmosClient(endpoint, credential=aad_credentials, consistency_level='Session')
        logging.info("Successfully connected to Cosmos DB using AAD default credential")
    except Exception as e:
        logging.error(f"Error connecting to Cosmos DB: {e}")
        return
    
    database_name = "ContosoDBDocIntellig"
    container_name = "Layouts"

    try:
        database = client.create_database_if_not_exists(database_name)
        logging.info(f"Database '{database_name}' does not exist. Creating it.")
    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(database_name)
        logging.info(f"Database '{database_name}' already exists.")

    database.read()
    logging.info(f"Reading into '{database_name}' DB")

    try:
        container = database.create_container(
            id=container_name,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )
        logging.info(f"Container '{container_name}' does not exist. Creating it.")
    except exceptions.CosmosResourceExistsError:
        container = database.get_container_client(container_name)
        logging.info(f"Container '{container_name}' already exists.")
    except exceptions.CosmosHttpResponseError:
        raise

    container.read()
    logging.info(f"Reading into '{container}' container")

    try:
        response = container.upsert_item(layout_data)
        logging.info(f"Saved processed layout data to Cosmos DB. Response: {response}")
    except Exception as e:
        logging.error(f"Error inserting item into Cosmos DB: {e}")

## MAIN 
@app.blob_trigger(arg_name="myblob", path="pdfinvoices/{name}",
                  connection="invoicecontosostorage_STORAGE")
def BlobTriggerContosoPDFLayoutsDocIntelligence(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob\n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    try:
        form_recognizer_client = initialize_form_recognizer_client()
        pdf_bytes = read_pdf_content(myblob)
        logging.info("Successfully read PDF content from blob.")
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return

    try:
        result = analyze_pdf(form_recognizer_client, pdf_bytes)
        logging.info("Successfully analyzed PDF using Document Intelligence.")
    except Exception as e:
        logging.error(f"Error analyzing PDF: {e}")
        return

    try:
        layout_data = extract_layout_data(result)
        logging.info("Successfully extracted layout data.")
    except Exception as e:
        logging.error(f"Error extracting layout data: {e}")
        return

    try:
        save_layout_data_to_cosmos(layout_data)
        logging.info("Successfully saved layout data to Cosmos DB.")
    except Exception as e:
        logging.error(f"Error saving layout data to Cosmos DB: {e}")
