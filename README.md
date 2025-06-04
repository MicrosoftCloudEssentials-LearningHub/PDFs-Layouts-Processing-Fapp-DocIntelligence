# Demo: PDF Layout Extraction with Doc Intelligence (full-code approach)

`Azure Storage + Document Intelligence + Function App +  Cosmos DB`

Costa Rica

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com)
[![GitHub](https://img.shields.io/badge/--181717?logo=github&logoColor=ffffff)](https://github.com/)
[brown9804](https://github.com/brown9804)

Last updated: 2025-06-03

----------

> [!IMPORTANT]
> This example is based on a `public network site and is intended for demonstration purposes only`. It showcases how several Azure resources can work together to achieve the desired result. Consider the section below about [Important Considerations for Production Environment](#important-considerations-for-production-environment). Please note that `these demos are intended as a guide and are based on my personal experiences. For official guidance, support, or more detailed information, please refer to Microsoft's official documentation or contact Microsoft directly`: [Microsoft Sales and Support](https://support.microsoft.com/contactus?ContactUsExperienceEntryPointAssetId=S.HP.SMC-HOME)

<details>
<summary><b>List of References</b> (Click to expand)</summary>

- [Azure AI Document Intelligence documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/?view=doc-intel-4.0.0)
- [Get started with the Document Intelligence Sample Labeling tool](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/v21/try-sample-label-tool?view=doc-intel-2.1.0#prerequisites-for-training-a-custom-form-model)
- [Document Intelligence Sample Labeling tool](https://fott-2-1.azurewebsites.net/)
- [Assign an Azure role for access to blob data](https://learn.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access?tabs=portal)
- [Build and train a custom extraction model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/build-a-custom-model?view=doc-intel-2.1.0)
- [Compose custom models - Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/compose-custom-models?view=doc-intel-2.1.0&tabs=studio)
- [Deploy the Sample Labeling tool](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/v21/deploy-label-tool?view=doc-intel-2.1.0)
- [Train a custom model using the Sample Labeling tool](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/v21/label-tool?view=doc-intel-2.1.0)
- [Train models with the sample-labeling tool](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/v21/supervised-table-tags?view=doc-intel-2.1.0)
- [Azure Cosmos DB - Database for the AI Era](https://learn.microsoft.com/en-us/azure/cosmos-db/introduction)
- [Consistency levels in Azure Cosmos DB](https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels)
- [Azure Cosmos DB SQL API client library for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/cosmos-readme?view=azure-python)
- [CosmosClient class documentation](https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos.cosmos_client.cosmosclient?view=azure-python)
- [Cosmos AAD Authentication](https://learn.microsoft.com/en-us/python/api/overview/azure/cosmos-readme?view=azure-python#aad-authentication)
- [Cosmos python examples](https://learn.microsoft.com/en-us/python/api/overview/azure/cosmos-readme?view=azure-python#examples)
- [Use control plane role-based access control with Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/security/how-to-grant-control-plane-role-based-access?tabs=built-in-definition%2Ccsharp&pivots=azure-interface-portal)
- [Use data plane role-based access control with Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/security/how-to-grant-data-plane-role-based-access?tabs=built-in-definition%2Ccsharp&pivots=azure-interface-cli)
- [Create or update Azure custom roles using Azure CLI](https://learn.microsoft.com/en-us/azure/role-based-access-control/custom-roles-cli)

</details>

> How to extract layout elements from PDFs stored in an Azure Storage Account, process them using Azure Document Intelligence, and store the results in Cosmos DB for further analysis.
>
> 1. Upload your PDFs to an Azure Blob Storage container. <br/>
> 2. An Azure Function is triggered by the upload, which calls the Azure Document Intelligence Layout API to analyze the document structure.  <br/>
> 3. The extracted layout data (such as tables, checkboxes, and text) is parsed and subsequently stored in a Cosmos DB database, ensuring a seamless and automated workflow from document upload to data storage.

> [!NOTE]
> Advantages of Document Intelligence for organizations handling with large volumes of documents: <br/>
>
> - Utilizes natural language processing, computer vision, deep learning, and machine learning. <br/>
> - Handles structured, semi-structured, and unstructured documents. <br/>
> - Automates the extraction and transformation of layout data into usable formats like JSON or CSV.

<div align="center">
  <img src="https://github.com/user-attachments/assets/f9096521-65a7-42f1-a641-953ec5a5c8f2" alt="Centered Image" style="border: 2px solid #4CAF50; border-radius: 5px; padding: 5px;"/>
</div>

## Important Considerations for Production Environment

<details>
  <summary>Private Network Configuration</summary>

 > For enhanced security, consider configuring your Azure resources to operate within a private network. This can be achieved using Azure Virtual Network (VNet) to isolate your resources and control inbound and outbound traffic. Implementing private endpoints for services like Azure Blob Storage and Azure Functions can further secure your data by restricting access to your VNet.

</details>

<details>
  <summary>Security</summary>

  > Ensure that you implement appropriate security measures when deploying this solution in a production environment. This includes: <br/>
  >
  > - Securing Access: Use Azure Entra ID (formerly known as Azure Active Directory or Azure AD) for authentication and role-based access control (RBAC) to manage permissions. <br/>
  > - Managing Secrets: Store sensitive information such as connection strings and API keys in Azure Key Vault. <br/>
  > - Data Encryption: Enable encryption for data at rest and in transit to protect sensitive information.

</details>

<details>
  <summary>Scalability</summary>

  > While this example provides a basic setup, you may need to scale the resources based on your specific requirements. Azure services offer various scaling options to handle increased workloads. Consider using: <br/>
  >
  > - Auto-scaling: Configure auto-scaling for Azure Functions and other services to automatically adjust based on demand. <br/>
  > - Load Balancing: Use Azure Load Balancer or Application Gateway to distribute traffic and ensure high availability.

</details>

<details>
  <summary>Cost Management</summary>

  > Monitor and manage the costs associated with your Azure resources. Use Azure Cost Management and Billing to track usage and optimize resource allocation.

</details>

<details>
  <summary>Compliance</summary>

  > Ensure that your deployment complies with relevant regulations and standards. Use Azure Policy to enforce compliance and governance policies across your resources.
</details>

<details>
  <summary>Disaster Recovery</summary>
   
> Implement a disaster recovery plan to ensure business continuity in case of failures. Use Azure Site Recovery and backup solutions to protect your data and applications.

</details>

## Prerequisites

- An `Azure subscription is required`. All other resources, including instructions for creating a Resource Group, are provided in this workshop.
- `Contributor role assigned or any custom role that allows`: access to manage all resources, and the ability to deploy resources within subscription.
- If you choose to use the Terraform approach, please ensure that:
  - [Terraform is installed on your local machine](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/install-cli#install-terraform).
  - [Install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) to work with both Terraform and Azure commands.

## Where to start? 

1. Please follow the [Terraform guide](./terraform-infrastructure/) to deploy the necessary Azure resources for the workshop.
2. Next, as this method `skips the creation of each resource` manually. Proceed with the configuration from [Configure/Validate the Environment variables](#function-app-configurevalidate-the-environment-variables).

> [!IMPORTANT]
> Regarding `Networking`, this example will cover `Public access configuration`, and `system-managed identity`. However, please ensure you `review your privacy requirements and adjust network and access settings as necessary for your specific case`.

## Overview 

> Using Cosmos DB provides you with a flexible, scalable, and globally distributed database solution that can handle both structured and semi-structured data efficiently. <br/>
>
> - `Azure Blob Storage`: Store the PDF invoices. <br/>
> - `Azure Functions`: Trigger on new PDF uploads, extract data, and process it. <br/>
> - `Azure SQL Database or Cosmos DB`: Store the extracted data for querying and analytics. <br/> 

| Resource                  | Recommendation                                                                                                      |
|---------------------------|----------------------------------------------------------------------------------------------------------------------|
| **Azure Blob Storage**    | Use for storing the PDF files. This keeps your file storage separate from your data storage, which is a common best practice. |
| **Azure SQL Database**    | Use if your data is highly structured and you need complex queries and transactions.                                  |
| **Azure Cosmos DB**       | Use if you need a globally distributed database with low latency and the ability to handle semi-structured data.      |

### Function App Hosting Options 

> In the context of Azure Function Apps, a `hosting option refers to the plan you choose to run your function app`. This choice affects how your function app is scaled, the resources available to each function app instance, and the support for advanced functionalities like virtual network connectivity and container support.

| **Plan**                | **Scale to Zero** | **Scale Behavior**                     | **Virtual Networking** | **Dedicated Compute & Reserved Cold Start** | **Max Scale Out (Instances)** | **Example AI Use Cases**                                                                 |
|-------------------------|-------------------|----------------------------------------|------------------------|---------------------------------------------|--------------------------------|------------------------------------------------------------------------------------------|
| **Flex Consumption**    | `Yes`             | `Fast event-driven`                    | `Optional`             | `Optional (Always Ready)`                   | `1000`                         | `Real-time data processing` for AI models, `high-traffic AI-powered APIs`, `event-driven AI microservices`. Use for applications needing to process large volumes of data in real-time, such as AI models for fraud detection or real-time recommendation systems. Ideal for deploying APIs that serve AI models, such as natural language processing (NLP) or computer vision services, which require rapid scaling based on demand. |
| **Consumption**         | `Yes`             | `Event-driven`                         | `Optional`             | `No`                                        | `200`                          | `Lightweight AI APIs`, `scheduled AI tasks`, `low-traffic AI event processing`. Suitable for deploying lightweight AI services, such as sentiment analysis or simple image recognition, which do not require extensive resources. Perfect for running periodic AI tasks, like batch processing of data for machine learning model training or scheduled data analysis. |
| **Functions Premium**   | `No`              | `Event-driven with premium options`    | `Yes`                  | `Yes`                                       | `100`                          | `Enterprise AI applications`, AI services requiring `VNet integration`, `low-latency AI APIs`. Use for mission-critical AI applications that require high availability, low latency, and integration with virtual networks, such as AI-driven customer support systems or advanced analytics platforms. Ideal for AI services that need to securely connect to on-premises resources or other Azure services within a virtual network. |
| **App Service**         | `No`              | `Dedicated VMs`                        | `Yes`                  | `Yes`                                       | `Varies`                       | `AI-powered web applications` with integrated functions, AI applications needing `dedicated resources`. Great for web applications that incorporate AI functionalities, such as personalized content delivery, chatbots, or interactive AI features. Suitable for AI applications that require dedicated compute resources for consistent performance, such as intensive data processing or complex AI model inference. |
| **Container Apps Env.** | `No`              | `Containerized microservices environment` | `Yes`                  | `Yes`                                       | `Varies`                       | `AI microservices architecture`, containerized AI workloads, `complex AI event-driven workflows`. Perfect for building a microservices architecture where each service can be independently scaled and managed, such as a suite of AI services for different tasks (e.g., image processing, text analysis). Ideal for deploying containerized AI workloads that need to run in a managed environment, such as machine learning model training and deployment pipelines. Suitable for orchestrating complex workflows involving multiple AI services and event-driven processes, such as automated data pipelines and real-time analytics. |

## Function App: Configure/Validate the Environment variables

> [!NOTE]
> This example is using system-assigned managed identity to assign RBACs (Role-based Access Control).


- Under `Settings`, go to `Environment variables`. And `+ Add` the following variables:

  - `COSMOS_DB_ENDPOINT`: Your Cosmos DB account endpoint 🡢 `Review the existence of this, if not create it`
  - `COSMOS_DB_KEY`: Your Cosmos DB account key 🡢 `Review the existence of this, if not create it`
  - `COSMOS_DB_CONNECTION_STRING`: Your Cosmos DB connection string 🡢 `Review the existence of this, if not create it`
  - `invoicecontosostorage_STORAGE`: Your Storage Account connection string 🡢 `Review the existence of this, if not create it`
  - `FORM_RECOGNIZER_ENDPOINT`: For example: `https://<your-form-recognizer-endpoint>.cognitiveservices.azure.com/` 🡢 `Review the existence of this, if not create it`
  - `FORM_RECOGNIZER_KEY`: Your Documment Intelligence Key (Form Recognizer). 🡢
  - `FUNCTIONS_EXTENSION_VERSION`: `~4` 🡢 `Review the existence of this, if not create it`
  - `WEBSITE_RUN_FROM_PACKAGE`: `1` 🡢 `Review the existence of this, if not create it`
  - `FUNCTIONS_WORKER_RUNTIME`: `python` 🡢 `Review the existence of this, if not create it`
  - `FUNCTIONS_NODE_BLOCK_ON_ENTRY_POINT_ERROR`: `true` (This setting ensures that all entry point errors are visible in your application insights logs). 🡢 `Review the existence of this, if not create it`

      <img width="550" alt="image" src="https://github.com/user-attachments/assets/31d813e7-38ba-46ff-9e4b-d091ae02706a">

      <img width="550" alt="image" src="https://github.com/user-attachments/assets/45313857-b337-4231-9184-d2bb46e19267">

      <img width="550" alt="image" src="https://github.com/user-attachments/assets/074d2fa5-c64d-43bd-8ed7-af6da46d86a2">

      <img width="550" alt="image" src="https://github.com/user-attachments/assets/ec5d60f3-5136-489d-8796-474b7250865d">

  - Click on `Apply` to save your configuration.
    
      <img width="550" alt="image" src="https://github.com/user-attachments/assets/437b44bb-7735-4d17-ae49-e211eca64887">

<div align="center">
  <h3 style="color: #4CAF50;">Total Visitors</h3>
  <img src="https://profile-counter.glitch.me/brown9804/count.svg" alt="Visitor Count" style="border: 2px solid #4CAF50; border-radius: 5px; padding: 5px;"/>
</div>
