import requests
from bs4 import BeautifulSoup
import os
import webbrowser

website_prefix = "https://www.aupairworld.com"

class AuPairWorldScraper:
    def __init__(self, url, txt_filename):
        self.url = url
        self.txt_filename = txt_filename
        self.saved_links = set()
        self.data = []

    def load_saved_links(self):
        if os.path.exists(self.txt_filename):
            with open(self.txt_filename, 'r') as file:
                self.saved_links = set(file.read().splitlines())

    def scrape_links(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        profiles = soup.find_all('div', class_='profile-details mt-2 medium-pl-1')

        for profile in profiles:
            link = profile.find('a', target='_blank')
            if link:
                href = link.get('href')
                if href not in self.saved_links:
                    self.saved_links.add(website_prefix + href)
                    self.data.append(website_prefix + href)

    def save_to_txt(self):
        if self.data:
            with open(self.txt_filename, 'a') as file:
                for link in self.data:
                    file.write(link + '\n')
            print(f'Data saved to {self.txt_filename}')
        else:
            print('No new data to save.')

    def scrape_and_save_new_links(self):
        self.load_saved_links()
        self.scrape_links()
        self.save_to_txt()

if __name__ == "__main__":
    link = website_prefix + "/en/find-family?field_nation_aupair_target_id=15419&field_gender_value=M&field_country_family_target_id%5B15930%5D=15930&field_start_date_min_value=202310&field_start_date_max_value=202311&field_duration_min_value=1&field_duration_max_value=4"
    txt_filename = "aupairworld_links.txt"

    scraper = AuPairWorldScraper(link, txt_filename)
    scraper.scrape_and_save_new_links()

    # Open the links that haven't been saved yet
    for link in scraper.data:
        webbrowser.open(link)
