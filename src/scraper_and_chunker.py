import requests
from bs4 import BeautifulSoup, Tag
import json
import os
import hashlib
from typing import List, Dict

def scrape_cleveland_clinic_page(url: str) -> List[Dict[str, str]]:
    """
    Scrapes content from a Cleveland Clinic page and chunks it by h3 headings.
    
    Args:
        url (str): URL of the Cleveland Clinic page
        
    Returns:
        List[Dict[str, str]]: List of chunks, each containing a heading and content
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        chunks = []
        current_chunk = {"heading": "", "content": ""}
        current_content = []
        
        # Process each element in the main content
        for element in soup.find_all(['h3', 'p', 'li', 'ul', 'ol']):
            # If we find an h3, start a new chunk
            if element.name == 'h3':
                # Save the previous chunk if it exists
                if current_chunk["heading"] or current_chunk["content"]:
                    current_chunk["content"] = "\n".join(current_content)
                    chunks.append(current_chunk.copy())
                
                # Start a new chunk
                current_chunk = {
                    "heading": element.get_text().strip(),
                    "content": ""
                }
                current_content = []
            
            # Add content to the current chunk
            else:
                text = element.get_text().strip()
                if text:
                    current_content.append(text)
        
        # Add the last chunk if it exists
        if current_chunk["heading"] or current_content:
            current_chunk["content"] = "\n".join(current_content)
            chunks.append(current_chunk)
        
        return chunks
    
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return []

def save_chunks_to_json(url: str, chunks: List[Dict[str, str]]) -> str:
    """
    Saves the chunks to a JSON file in the corpus directory.
    
    Args:
        url (str): Original URL of the content
        chunks (List[Dict[str, str]]): List of chunks with headings and content
        
    Returns:
        str: Path to the saved JSON file
    """
    # Create corpus directory if it doesn't exist
    corpus_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'corpus')
    os.makedirs(corpus_dir, exist_ok=True)
    
    # Create a filename based on the URL
    url_hash = hashlib.md5(url.encode()).hexdigest()
    filename = f"cleveland_clinic_{url_hash}.json"
    filepath = os.path.join(corpus_dir, filename)
    
    # Prepare the data structure
    data = {
        "source_url": url,
        "chunks": chunks
    }
    
    # Save to JSON file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filepath

def process_cleveland_clinic_page(url: str) -> str:
    """
    Main function to process a Cleveland Clinic page: scrape, chunk by h3 headings, and save.
    
    Args:
        url (str): URL of the Cleveland Clinic page
        
    Returns:
        str: Path to the saved JSON file
    """
    # Scrape the content and get chunks
    chunks = scrape_cleveland_clinic_page(url)
    if not chunks:
        raise ValueError(f"Failed to scrape content from {url}")
    
    # Save chunks to JSON
    output_file = save_chunks_to_json(url, chunks)
    return output_file

def main():
    # Example usage
    URLS = [
        # "https://my.clevelandclinic.org/health/treatments/22060-angioplasty",
        # "https://my.clevelandclinic.org/health/diseases/21501-type-2-diabetes",
        # "https://my.clevelandclinic.org/health/diseases/7104-diabetes",
        # "https://my.clevelandclinic.org/health/diseases/4314-hypertension-high-blood-pressure",
        # "https://my.clevelandclinic.org/health/diseases/15096-chronic-kidney-disease",
        # "https://my.clevelandclinic.org/health/articles/11920-cholesterol-numbers-what-do-they-mean",
        # "https://my.clevelandclinic.org/health/diseases/16898-coronary-artery-disease",
        # "https://my.clevelandclinic.org/health/drugs/20966-metformin-tablets",
        # "https://my.clevelandclinic.org/health/diseases/9290-depression",
        # "https://my.clevelandclinic.org/health/drugs/19162-lisinopril-tablets",
        # "https://my.clevelandclinic.org/health/drugs/19081-atorvastatin-tablets",
        # "https://my.clevelandclinic.org/health/drugs/20592-aspirin-tablets",
        # "https://my.clevelandclinic.org/health/diseases/pollen-allergy",
        # "https://my.clevelandclinic.org/health/symptoms/8106-nausea--vomiting",
        # "https://my.clevelandclinic.org/health/articles/10881-vital-signs",
        # "https://my.clevelandclinic.org/health/procedures/21922-appendectomy",
        # "https://my.clevelandclinic.org/health/diseases/15572-cirrhosis-of-the-liver",
        # "https://my.clevelandclinic.org/health/procedures/21614-gallbladder-removal",
        # "https://my.clevelandclinic.org/health/drugs/18057-furosemide-tablets",
        # "https://my.clevelandclinic.org/health/drugs/19755-spironolactone-tablets",
        # "https://my.clevelandclinic.org/health/drugs/20231-propranolol-tablets",
        # "https://my.clevelandclinic.org/health/diseases/3909-alcoholism",
    ]
    for url in URLS:
        try:
            output_file = process_cleveland_clinic_page(url)
            print(f"Successfully processed page. Output saved to: {output_file}")
        except Exception as e:
            print(f"Error processing page: {str(e)}")

if __name__ == "__main__":
    main()
