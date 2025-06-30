# Blogs Contents Classification

This project aims to classify blog content based on predefined categories or topics using the Gemini API. It processes a list of URLs and a list of diseases to identify which diseases are mentioned in each blog post based on specific criteria.

## 📦 Requirements

*   Python 3.x
*   Required Python libraries: `pandas`, `google-generativeai`
*   A valid Google Gemini API Key
*   Internet connection to access URLs and the Gemini API

## 🔧 Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/liemnh98/Mentioned-Diseases-in-VNVC-Articles.git
cd Mentioned-Diseases-in-VNVC-Articles
```

### 2. Create and activate a virtual environment

#### On Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### On macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Gemini API Key

Create a directory named `keys` in the project root if it doesn't exist.
Inside the `keys` directory, create a file named `Gemini_API_Key.txt` and paste your Gemini API key into this file.

```
keys/Gemini_API_Key.txt
```
The Gemini API key can be generated from [here]("https://aistudio.google.com/apikey").

## 📥 Input & Output

The script expects specific input files and generates an output file in the `data_demo` directory.

### Input Files

1.  **URLs File:** A CSV file containing the URLs to be processed.
    *   Default path: `data_demo/input/urls_test.csv`
    *   Must contain a column named `destinationURL_cleaned`.

    Example (`data_demo/input/urls_test.csv`):

    ```csv
    destinationURL_cleaned
    https://www.example.com/blog/post1
    https://www.example.com/article/xyz
    ```

2.  **Diseases File:** An Excel file containing the list of diseases to check against.
    *   Default path: `data_demo/input/TenNhomBenh.xlsx`
    *   Must contain a column named `TenNhomBenh`.

    Example (`data_demo/input/TenNhomBenh.xlsx`):

    | TenNhomBenh |
    |-------------|
    | Disease A   |
    | Disease B   |
    | Disease C   |

Ensure the `data_demo/input` directory exists and contains these files with the specified structure. You can update the `urls_dir` and `diseases_dir` variables in the script if your files are located elsewhere.

### Output File

A CSV file containing the mapping of URLs to the diseases identified in the content.

*   Default path: `data_demo/output/mapping_results_test.csv`
*   Columns: `url`, `disease`, `total_diseases`

Example (`data_demo/output/mapping_results_test.csv`):

```csv
url,disease,total_diseases
https://www.example.com/blog/post1,Disease A,2
https://www.example.com/blog/post1,Disease C,2
https://www.example.com/article/xyz,Disease B,1
```

Ensure the `data_demo/output` directory exists before running the script. You can update the `mapping_output_dir` variable in the script if you want to save the output elsewhere.

## ▶️ Run the Script

Once everything is set up, the API key is in place, and your input files are ready in the `data_demo/input` directory, run the main script:

```bash
python Gemini_Based_Article_Classification.py
```

The script will process each URL, query the Gemini API, and save the results to the specified output file. Progress will be printed to the console.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙋 Author

Liem ("Liam") Nguyen Huu.
