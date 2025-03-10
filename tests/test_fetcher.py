import pytest
from pubmed_fetcher.fetcher import fetch_pubmed_papers

def test_fetch_pubmed_papers():
    query = "cancer treatment"
    results = fetch_pubmed_papers(query, max_results=5)
    
    # Ensure we get a list
    assert isinstance(results, list)
    
    # Ensure each result has expected keys
    for paper in results:
        assert "PubmedID" in paper
        assert "Title" in paper
        assert "Publication Date" in paper
        assert "Authors" in paper
        assert "Affiliations" in paper
        assert "Corresponding Author Email" in paper

def test_empty_query():
    with pytest.raises(ValueError):
        fetch_pubmed_papers("")
