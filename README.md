# LangChain RAG with Chroma

## Description

This project,  is a Python-based application focused on Retrieval Augmented Generation (RAG). It leverages a ChromaDB vector store for efficient data retrieval and includes components for data handling, embedding models, and a core library for its functionalities. This project does use ollama nomic-embed-text:latest for the embedding model. Therefore to run the project as is you would have to setup ollama and pull the embedding.

## Features

*   **Retrieval Augmented Generation (RAG):** Core functionality for generating responses augmented with retrieved information.
*   **ChromaDB Integration:** Utilizes ChromaDB for vector storage and retrieval, enabling semantic search and context provision.
*   **Modular Design:** Organized into distinct directories for data, embedding models, and core library components.
*   **Python-based:** Developed entirely in Python, making it accessible and extensible within the Python ecosystem.

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Duanes-Tech-Hub/LangChain.RAG.With.Chroma.git
    cd RAGLang
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Setup: Ollama and nomic-embed-text for RAG
1. **Install Ollama on Windows**
Ollama for Windows is distributed as a single executable that includes everything needed to run models locally.

Download the Installer: Visit the official Ollama website and download the Windows installer: https://ollama.com/download/windows

Run Installation: Double-click the downloaded file (e.g., OllamaSetup.exe) and follow the installation prompts. The installer sets up the Ollama service to run automatically in the background.

Verify Installation: Open your Command Prompt or PowerShell and type the following command to check if the installation was successful:

```bash
ollama --version
```
If successful, you should see the installed version number. An Ollama icon will also appear in your system tray, confirming the background service is running.

2. **Pull the nomic-embed-text Model**
The nomic-embed-text model is an embedding model, which is specifically designed for generating the vector embeddings needed for your RAG system's retrieval step.

Execute the Pull Command: In your Command Prompt or PowerShell, use the ollama pull command to download and install the model:
```bash
ollama pull nomic-embed-text
```
Ollama will automatically download the necessary model files.

Note: This model is typically around 370 MB (for the latest version, such as nomic-embed-text:latest), so the download may take a few moments depending on your internet connection.

Verify Model Installation: To confirm the model is available, you can list your local models:

Bash

ollama list
You should see nomic-embed-text in the list of installed models.

## Usage

To run the main application, execute the `main.py` file:

```bash
python main.py
```

Further usage instructions and examples will be provided as the project develops.

## Project Structure

*   `main.py`: The main entry point of the application.
*   `requirements.txt`: Lists all Python dependencies required for the project.
*   `chroma/`: Directory containing the ChromaDB vector store data.
*   `data/`: Placeholder for raw or processed data used by the application.
*   `emodels/`: Contains embedding models or related configurations.
*   `library/`: Core library modules and helper functions.
    *   `cdb.py`: Likely handles ChromaDB interactions.
    *   `genlib.py`: General utility functions or generation-related logic.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.