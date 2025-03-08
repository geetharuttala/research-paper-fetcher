# **PubMed Fetcher**  

## **Overview**  
PubMed Fetcher is a command-line tool that retrieves research paper details from PubMed based on user queries. It processes the fetched data, filters academic and non-academic authors, and saves the results in a CSV file.



## **Project Structure**  
```
pubmed_fetcher/
│── src/
│   ├── pubmed_fetcher/
│   │   ├── __init__.py  
│   │   ├── cli.py  # Command-line interface
│   │   ├── fetcher.py  # Fetches data from PubMed
│   │   ├── filter.py  # Filters non-academic authors
│── tests/
│   ├── __init__.py  # Test cases (to be added)
│── pyproject.toml  # Dependency and project config
│── README.md  # Documentation
```



## **Installation and Setup**  

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/<your-username>/pubmed_fetcher.git
cd pubmed_fetcher
```

### **2️⃣ Install Dependencies using Poetry**
Ensure [Poetry](https://python-poetry.org/docs/) is installed, then run:
```sh
poetry install
```
This sets up a virtual environment and installs all required packages.

### **3️⃣ Run the Program**
To fetch research papers on a topic, use:
```sh
get-papers-list "machine learning"
```
If the command is not recognized, try:
```sh
poetry run get-papers-list "machine learning"
```

### **4️⃣ Command-Line Options**
| Option | Description |
|--------|-------------|
| `-h` or `--help` | Show help and usage details |
| `-d` or `--debug` | Print debug information |
| `-f` or `--file filename.csv` | Save output to a specified CSV file |



## **Technologies & Libraries Used**  

1. **[Biopython](https://biopython.org/)** – For fetching research papers from PubMed.
2. **[Pandas](https://pandas.pydata.org/)** – For handling CSV data.
3. **[Requests](https://docs.python-requests.org/en/latest/)** – For API requests.
4. **[Click](https://click.palletsprojects.com/)** – For CLI commands.
5. **[Poetry](https://python-poetry.org/)** – For dependency management.


## **Future Enhancements**
- Integrating an **LLM** to classify papers more efficiently.
- Adding unit tests to ensure reliability.

