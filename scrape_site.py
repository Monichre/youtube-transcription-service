import requests
from bs4 import BeautifulSoup


def scrape_webpage_to_file(url, output_file):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the webpage
        page_text = soup.get_text()

        # Write the content to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(page_text)

        print(f"Content successfully scraped and saved to {output_file}")
    else:
        print(
            f"Failed to retrieve the webpage. Status code: {response.status_code}")

# # Example usage
# url = 'https://example.com'
# output_file = 'webpage_content.txt'
# scrape_webpage_to_file(url, output_file)
