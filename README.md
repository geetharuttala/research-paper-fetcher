# **PubMed Fetcher**  

## **Overview**  
**PubMed Fetcher** is a command-line tool that retrieves research paper details from **PubMed** based on user queries. It processes the fetched data, filters academic and non-academic authors, and saves the results in a structured CSV file.  

This tool is designed to:  
1. Fetch research paper details using PubMed API.  
2. Identify **academic vs. non-academic** authors using heuristics.  
3. Save output in a CSV file for easy analysis.  



## **Project Structure**  
```
pubmed_fetcher/
│── dist/                 # Contains distribution packages (for PyPI/TestPyPI)
│── src/
│   ├── pubmed_fetcher/
│   │   ├── __init__.py  
│   │   ├── cli.py        # Command-line interface  
│   │   ├── fetcher.py    # Fetches data from PubMed  
│   │   ├── filter.py     # Filters non-academic authors  
│── tests/
│   ├── __init__.py       # Test cases  
│   ├── test_cli.py       # Tests CLI functionality  
│   ├── test_fetcher.py   # Tests fetching logic  
│   ├── test_filter.py    # Tests filtering logic  
│── pyproject.toml        # Dependency and project config  
│── README.md             # Documentation  
```
 **Note:** The `dist/` folder contains the packaged distribution files when the project is built using:  
```powershell
poetry build
```
These files are used for uploading to **PyPI or TestPyPI**.



## **Installation and Setup**  

### **1️⃣ Install via TestPyPI (Recommended for Testing)**  
The package is available on **TestPyPI**. To install it, run:  
```powershell
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pubmed-fetcher-geetha
```

### **2️⃣ Install from Source (Development Mode)**  
Alternatively, you can clone the repository and install dependencies manually.  

```powershell
git clone https://github.com/<geetharuttala>/pubmed_fetcher.git
cd pubmed_fetcher
poetry install
```
This sets up a virtual environment and installs all required packages.  



## **Usage**  

### **Fetching Research Papers**
To fetch research papers on a topic, use:  
```powershell
get-papers-list "diabetes"
```

To specify an output file for saving results:  
```powershell
get-papers-list "breast cancer" -f output.csv
```

 **Note:**  
- The output **CSV file** will be saved in the **same directory** where you run the command.  
- If the command is not recognized, try:  
  ```powershell
  poetry run get-papers-list "cancer"
  ```



## **Command-Line Options**  
| **Option** | **Description** |  
|------------|----------------|  
| `-h` or `--help` | Show help and usage details |  
| `-d` or `--debug` | Print debug information |  
| `-f` or `--file filename.csv` | Save output to a specified CSV file |  



## **Testing**
The project includes **unit tests** to ensure functionality. To run the tests:
```powershell
pytest
```
This will execute tests from the `tests/` directory.



## **Tools and Libraries Used**  
- **[Poetry](https://python-poetry.org/)** – Manages dependencies and packaging.  
- **[pytest](https://docs.pytest.org/)** – For running test cases.  
- **[requests](https://docs.python-requests.org/)** – Handles API requests to fetch research papers.  
- **[argparse](https://docs.python.org/3/library/argparse.html)** – Parses command-line arguments.  
- **[csv](https://docs.python.org/3/library/csv.html)** – Handles CSV file operations.  
- **[re](https://docs.python.org/3/library/re.html)** – Used for filtering non-academic authors based on heuristics.  



## **Future Enhancements**  
- **LLM Integration:** Enhance paper classification using a **local LLM model**.  
- **Unit Tests:** Add test cases for better reliability.  



## **Development and Contribution**  
If you wish to contribute:  
1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature-name`).  
3. Commit your changes (`git commit -m "Add feature"`).  
4. Push to GitHub and submit a Pull Request.  

## **License**
 This project is licensed under the MIT License.
