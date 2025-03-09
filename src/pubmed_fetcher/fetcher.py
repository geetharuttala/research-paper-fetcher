from typing import List, Dict, Union
from Bio import Entrez, Medline
import csv
import re
import time
from io import StringIO

Entrez.email = "geetharuttala0106@gmail.com"

def fetch_pubmed_papers(query: str, max_results: int = 2000, debug: bool = False) -> List[Dict]:
    """
    Fetches research papers from PubMed based on the given query.

    Args:
        query (str): Search query for PubMed.
        max_results (int): Maximum number of papers to fetch.

    Returns:
        List[Dict]: A list of parsed research papers.
    """
    try:
        if not query.strip():
            raise ValueError("Query cannot be empty.")
        
        if debug:
            print(f"🔍 Debug: Searching PubMed for '{query}' with max_results={max_results}")

        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="pub+date")
        record = Entrez.read(handle)
        handle.close()

        pmids = record.get("IdList", [])
        if not pmids:
            print("⚠️ No papers found for the given query.")
            return []
        
        if debug:
            print(f"🔍 Debug: Found {len(pmids)} papers matching query")

        # Fetch full paper details
        try:
            handle = Entrez.efetch(db="pubmed", id=",".join(pmids), rettype="medline", retmode="text")
            raw_data = handle.read()
            handle.close()
        except Exception as e:
            print(f"⚠️ Error fetching details for IDs: {e}")
            return []

        records = Medline.parse(StringIO(raw_data))  # ✅ Use StringIO to parse correctly
        results = parse_pubmed_data(records)
        
        if debug:
            print(f"🔍 Debug: Successfully parsed {len(results)} papers")

        return results

    except ValueError as ve:
        print(f"⚠️ Input Error: {ve}")
    except Exception as e:
        print(f"❌ Error fetching data from PubMed: {e}")

    return []



def parse_pubmed_data(records) -> List[Dict]:
    """
    Parses raw PubMed MEDLINE data into structured format.

    Args:
        records: Parsed MEDLINE records.

    Returns:
        List[Dict]: A list of dictionaries containing paper details.
    """
    results = []
    
    for record in records:
        try:
            pubmed_id = record.get("PMID", "N/A")
            title = record.get("TI", "N/A")
            pub_date = record.get("DP", "N/A")
            authors = record.get("AU", [])
            affiliations = record.get("AD", [])

            if not isinstance(authors, list):
                authors = ["N/A"]
            if not isinstance(affiliations, list):
                affiliations = ["N/A"]

            email = extract_email(affiliations)

            results.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Authors": authors,
                "Affiliations": affiliations,
                "Corresponding Author Email": email
            })

        except Exception as e:
            print(f"⚠️ Error parsing a record: {e}")

    return results



def extract_email(affiliation: Union[str, list]) -> str:
    """
    Extracts an email address from affiliation details using regex.

    Args:
        affiliation (str | list): Author's affiliation(s).

    Returns:
        str: Extracted email or "N/A" if not found.
    """
    if isinstance(affiliation, list):  
        affiliation = " ".join(affiliation)

    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation)
    return match.group(0) if match else "N/A"


import csv
from typing import List, Dict

def save_to_csv(data: List[Dict], filename: str = "pubmed_results.csv") -> None:
    """
    Saves the fetched PubMed data to a CSV file with proper formatting.

    Args:
        data (List[Dict]): List of research paper details.
        filename (str): Name of the output CSV file.

    Returns:
        None
    """
    if not data:
        print("⚠️ No data to save.")
        return

    columns = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns, quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for row in data:
                row["Non-academic Author(s)"] = ", ".join(row["Non-academic Author(s)"]) if isinstance(row["Non-academic Author(s)"], list) else row["Non-academic Author(s)"]
                row["Company Affiliation(s)"] = ", ".join(row["Company Affiliation(s)"]) if isinstance(row["Company Affiliation(s)"], list) else row["Company Affiliation(s)"]

                writer.writerow(row)

        print(f"✅ Data successfully saved to {filename}")

    except PermissionError:
        print(f"❌ Permission Error: Cannot write to {filename}. Check file permissions.")
    except IOError as e:
        print(f"❌ I/O Error: {e}")
