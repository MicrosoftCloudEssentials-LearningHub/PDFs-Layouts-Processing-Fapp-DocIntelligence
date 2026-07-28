document.addEventListener("DOMContentLoaded", () => {
  const logo = document.querySelector("a.md-logo");

  if (logo) {
    logo.href = new URL("./", document.baseURI).href;
  }
});