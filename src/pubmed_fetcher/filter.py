import re
from typing import List, Dict

# Non-academic email domains
NON_ACADEMIC_DOMAINS = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "protonmail.com"}

# Academic keywords (including common variations)
ACADEMIC_KEYWORDS = {
    r"\bUniversity\b", r"\bUniversit[a-z]*\b", r"\bCollege\b", r"\bSchool of\b", r"\bAcademy\b",
    r"\bFaculty of\b", r"\bDepartment of\b", r"\bInstitute of Technology\b", r"\bMedical School\b",
    r"\bTeaching Hospital\b", r"\bUniversitario\b"
}

# Company-related keywords
COMPANY_KEYWORDS = {
    r"\bInc\b", r"\bLtd\b", r"\bCorp\b", r"\bPharma\b", r"\bTechnologies\b", r"\bSolutions\b", r"\bLLC\b",
    r"\bConsulting\b", r"\bBiotech\b", r"\bLaboratories\b", r"\bDiagnostics\b", r"\bTherapeutics\b",
    r"\bBiosciences\b", r"\bResearch Institute\b"
}

def is_company_affiliation(affiliation: str) -> bool:
    """
    Determines if an affiliation belongs to a company while excluding academic institutions.

    Args:
        affiliation (str): Author's affiliation.

    Returns:
        bool: True if it's a company, False otherwise.
    """
    if not affiliation or affiliation == "N/A":
        return False

    # ✅ Check for academic institutions (match variations like "Universiti", "Universitario")
    if any(re.search(keyword, affiliation, re.IGNORECASE) for keyword in ACADEMIC_KEYWORDS):
        return False  # Exclude academic affiliations

    # ✅ Check if it's a company-affiliated research institute
    return any(re.search(keyword, affiliation, re.IGNORECASE) for keyword in COMPANY_KEYWORDS)

def extract_non_academic_authors(authors: List[str], affiliations: List[str]) -> List[str]:
    """
    Identifies non-academic authors based on their affiliations.

    Args:
        authors (List[str]): List of authors.
        affiliations (List[str]): List of affiliations.

    Returns:
        List[str]: Non-academic authors.
    """
    non_academic_authors = []

    for author, affiliation in zip(authors, affiliations):
        if is_company_affiliation(affiliation):  # ✅ Only consider non-academic authors from companies
            non_academic_authors.append(author)

    return non_academic_authors

def filter_non_academic_authors(data: List[Dict], debug: bool = False) -> List[Dict]:
    """
    Filters research papers to extract non-academic authors, keeping only relevant papers.

    Args:
        data (List[Dict]): List of research paper details.

    Returns:
        List[Dict]: Processed data with only relevant fields.
    """
    filtered_data = []
    
    for entry in data:
        authors = entry.get("Authors", [])
        affiliations = entry.get("Affiliations", [])
        email = entry.get("Corresponding Author Email", "N/A")

        # Extract company affiliations
        company_affiliations = [aff for aff in affiliations if is_company_affiliation(aff)]

        # 🔴 Ensure we only keep papers with company affiliations
        if not company_affiliations:
            continue  # Skip this paper if no company affiliations are found ✅

        # Extract non-academic authors (company-affiliated ones)
        non_academic_authors = extract_non_academic_authors(authors, affiliations)

        # ✅ Now, this ensures that "Company Affiliation(s)" is **never N/A**
        filtered_data.append({
            "PubmedID": entry["PubmedID"],
            "Title": entry["Title"],
            "Publication Date": entry["Publication Date"],
            "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Company Affiliation(s)": ", ".join(company_affiliations),
            "Corresponding Author Email": email,
        })
        
    if debug:
        print(f"🔍 Debug: Filtered {len(filtered_data)} papers with company affiliations")
 
    return filtered_data
