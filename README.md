# litollama

Explore and Use Ollama with a Streamlit App!

## Overview
`litollama` is a Streamlit-based application that allows you to interact with large language models using Ollama. This guide will walk you through the steps to set up and run the application on your local machine.

## Prerequisites
Before you start, ensure you have the following installed:
- Python 3.7 or higher
- `pip` (Python package installer)

## Installation Steps

### 1. Download and Install Ollama
1. Visit [Ollama](https://ollama.com/) to download the latest version of the software.
2. Follow the installation instructions provided on the website.

### 2. Run Ollama with `llama3`
1. Open a terminal or command prompt.
2. Execute the following command to download and run the `llama3` model:
   ```sh
   ollama run llama3
   ```
You may install other models by replacing `llama3` with your desired model name. Visit https://ollama.com/library.html for more information on available models.

### 3. Clone the Repository
Clone this `litollama` repository to your local machine using the following command:
```sh
git clone https://github.com/ineelhere/litollama.git
```

### 4. Set Up the Python Environment
Navigate to the cloned repository and create a virtual environment:
```sh
cd litollama
python -m venv venv
```
Activate the virtual environment:
- On Windows:
  ```sh
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```sh
  source venv/bin/activate
  ```

### 5. Install the Required Packages
Install the dependencies listed in the `requirements.txt` file:
```sh
pip install -r requirements.txt
```

### 6. Run the Streamlit App
Start the Streamlit app by running:
```sh
streamlit run app.py
```

## Usage
Once the app is running, open your web browser and navigate to the URL provided in the terminal (typically `http://localhost:8501`). You can now interact with the `llama3` model through the Streamlit interface.

You may also install other models to run with ollama. Visit https://ollama.com/library.

## Contributing
Please fork the repository, create a new branch, and submit a pull request with your changes.

Enjoy using `litollama`! If you encounter any issues or have suggestions for improvement, feel free to open an issue on GitHub.