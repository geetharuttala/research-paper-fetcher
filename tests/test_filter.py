from pubmed_fetcher.filter import filter_non_academic_authors, is_company_affiliation

def test_is_company_affiliation():
    assert is_company_affiliation("XYZ Pharma Inc") == True
    assert is_company_affiliation("Harvard University") == False
    assert is_company_affiliation("N/A") == False

def test_filter_non_academic_authors():
    sample_data = [
        {
            "PubmedID": "12345",
            "Title": "Test Paper",
            "Publication Date": "2023",
            "Authors": ["Dr. Alice", "Dr. Bob"],
            "Affiliations": ["XYZ Pharma Inc", "Harvard University"],
            "Corresponding Author Email": "alice@xyzpharma.com"
        }
    ]

    filtered_data = filter_non_academic_authors(sample_data)
    
    assert len(filtered_data) == 1  # Should return one paper
    assert filtered_data[0]["Non-academic Author(s)"] == "Dr. Alice"
    assert filtered_data[0]["Company Affiliation(s)"] == "XYZ Pharma Inc"


