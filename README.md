# prodigal-assignment

# Debt Collection Call Analysis Tool

## 📖 Overview

[cite_start]This project provides a comprehensive tool for analyzing audio conversations between debt collection agents and borrowers. [cite: 2] [cite_start]The primary goal is to automatically evaluate these conversations for **profanity**, **privacy compliance violations**, and key **call quality metrics** like overtalk and silence percentage. [cite: 3] [cite_start]The tool is built as a Streamlit application, allowing users to upload individual call transcripts in YAML format and analyze them using different methodologies. [cite: 4, 34, 36]

---

## ✨ Features

* [cite_start]**Profanity Detection**: Identifies calls containing profane language from either the agent or the borrower. [cite: 13]
* [cite_start]**Privacy & Compliance Violation**: Detects instances where agents share sensitive account information *before* properly verifying the borrower's identity. [cite: 16, 17, 18]
* **Call Quality Metrics**: Calculates and visualizes two key metrics:
    * [cite_start]**Overtalk Percentage**: The percentage of the call where both parties are speaking simultaneously. [cite: 20]
    * [cite_start]**Silence Percentage**: The percentage of the call where neither party is speaking. [cite: 21]
* **Multiple Analysis Approaches**: For Profanity and Compliance detection, the application allows users to choose between:
    * [cite_start]A fast and simple **Pattern Matching (Regex)** approach. [cite: 27]
    * [cite_start]A more context-aware **Machine Learning (Fine-tuned LLM)** approach. [cite: 31]
* [cite_start]**Interactive Web Application**: A user-friendly interface built with Streamlit for easy file uploads and analysis selection. [cite: 34]

---

## 🛠️ Tech Stack

* **Backend**: Python
* **Web Framework**: Streamlit
* **Data Handling**: PyYAML, Pandas
* **NLP/ML**: Scikit-learn, Transformers (Hugging Face), NLTK, spaCy
* **Pattern Matching**: `re` (Regex)
* **Visualization**: Matplotlib, Seaborn, Plotly

---

## 🚀 Setup and Execution

Follow these steps to set up and run the project on your local machine.

### Prerequisites

* Python 3.8+
* pip (Python package installer)
* Git

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare the Data:**
    * [cite_start]The project expects conversation data in YAML files, where the filename is the call ID. [cite: 6, 7]
    * Place your YAML files inside a `data/` directory in the root of the project.

### Running the Application

1.  **Launch the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
2.  Your web browser should open with the application running.

---

## 🖥️ How to Use the App

1.  [cite_start]**Upload a Call File**: Use the file uploader to select a single call conversation in `.yaml` format from your local machine. [cite: 36]
2.  [cite_start]**Select Analysis Type**: Use the first dropdown to choose the entity you want to detect: **Profanity** or **Privacy & Compliance Violation**. [cite: 39]
3.  [cite_start]**Select Approach**: Use the second dropdown to choose the detection method: **Pattern Matching** or **Machine Learning**. [cite: 38]
4.  [cite_start]**View Results**: The application will process the file and output a flag indicating the presence or absence of the selected entity. [cite: 40]
5.  [cite_start]**View Metrics**: The visualizations for overtalk and silence percentage will be displayed separately. [cite: 42]

---

## 📁 Project Structure
