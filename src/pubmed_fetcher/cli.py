import argparse
from pubmed_fetcher.fetcher import fetch_pubmed_papers, save_to_csv
from pubmed_fetcher.filter import filter_non_academic_authors

def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed and filter non-academic authors.",
        epilog=(
            "Installation & Usage:\n"
            "  1️⃣ Install Dependencies:\n"
            "     Ensure Poetry is installed, then run:\n"
            "         poetry install\n\n"
            "  2️⃣ Run the Program:\n"
            "     Fetch research papers on a topic using:\n"
            "         get-papers-list \"machine learning\"\n\n"
            "     If the command is not recognized, try:\n"
            "         poetry run get-papers-list \"machine learning\"\n\n"
            "Example:\n"
            "  get-papers-list \"lung cancer\" -f results.csv"
        ),
        formatter_class=argparse.RawTextHelpFormatter  # ✅ Ensures multiline help formatting
    )

    parser.add_argument("query", type=str, help="Search query for PubMed (e.g., 'cancer & healthcare')")
    parser.add_argument("-f", "--file", type=str, nargs="?", help="Output CSV filename (leave empty to print to console)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode to print extra logs")

    args = parser.parse_args()

    # Fetch data from PubMed
    papers = fetch_pubmed_papers(args.query, debug=args.debug)

    if not papers:
        print("⚠️ No research papers found.")
        return

    # Filter non-academic authors
    filtered_papers = filter_non_academic_authors(papers)
    
    # Debug: Show count of papers before and after filtering
    if args.debug:
        print(f"🔍 Debug: Fetched {len(papers)} papers, after filtering: {len(filtered_papers)}")

    # Save results or print to console
    if args.file:
        save_to_csv(filtered_papers, args.file)
        print(f"✅ Filtered data saved to {args.file}")
    else:
        print("📄 Filtered Research Papers:")
        for paper in filtered_papers:
            print(f"🔹 PubmedID: {paper.get('PubmedID', 'Unknown')}")
            print(f"   Title: {paper.get('Title', 'No Title')}")
            print(f"   Publication Date: {paper.get('Publication Date', 'N/A')}")
            print(f"   Non-academic Authors: {paper.get('Non-academic Author(s)', 'N/A')}")
            print(f"   Company: {paper.get('Company Affiliation(s)', 'N/A')}")
            print(f"   Corresponding Author Email: {paper.get('Corresponding Author Email', 'N/A')}")
            print("-" * 80) 

if __name__ == "__main__":
    main()
