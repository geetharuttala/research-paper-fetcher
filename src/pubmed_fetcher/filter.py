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

    # Check if ANY part of the affiliation is academic
    if any(re.search(keyword, affiliation, re.IGNORECASE) for keyword in ACADEMIC_KEYWORDS):
        return False  # Exclude academic affiliations

    # Check if ANY part of the affiliation is a company
    return any(re.search(keyword, affiliation, re.IGNORECASE) for keyword in COMPANY_KEYWORDS)

def extract_non_academic_authors(authors: List[str], affiliations: List[str]) -> List[str]:
    """
    Identifies non-academic authors **who have at least one biotech/pharma company affiliation**.

    Args:
        authors (List[str]): List of authors.
        affiliations (List[str]): List of affiliations.

    Returns:
        List[str]: List of authors with company affiliations.
    """
    non_academic_authors = []

    for author, aff in zip(authors, affiliations):
        if not aff or aff == "N/A":
            continue  # Skip empty affiliations

        # 🔹 Handle multiple affiliations properly
        aff_list = re.split(r';|,|\band\b', aff)  # Splitting affiliations
        has_company_affiliation = any(is_company_affiliation(a.strip()) for a in aff_list)

        if has_company_affiliation:
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

        # ✅ Extract unique company affiliations
        company_affiliations = list(set(
            aff.strip() for aff in affiliations for part in re.split(r';|,|\band\b', aff)
            if is_company_affiliation(part.strip())
        ))

        # ✅ Ensure we only keep papers with company affiliations
        if not company_affiliations:
            continue  # Skip this paper if no company affiliations are found

        # ✅ Extract non-academic authors (company-affiliated ones)
        non_academic_authors = extract_non_academic_authors(authors, affiliations)

        # ✅ Ensure papers without non-academic authors are NOT included
        if not non_academic_authors:
            continue  # Skip this paper if no authors match

        filtered_data.append({
            "PubmedID": entry["PubmedID"],
            "Title": entry["Title"],
            "Publication Date": entry["Publication Date"],
            "Non-academic Author(s)": ", ".join(non_academic_authors),
            "Company Affiliation(s)": ", ".join(company_affiliations),
            "Corresponding Author Email": email,
        })
        
    if debug:
        print(f"🔍 Debug: Filtered {len(filtered_data)} papers with company affiliations and valid authors")
 
    return filtered_data
