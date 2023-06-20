import argparse
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from colorama import Fore, Style


def check_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.netloc and parsed_url.netloc.count('.'))


class Browser:
    def __init__(self):
        self.saved_files = []
        self.my_stack = deque()

        parser = argparse.ArgumentParser()
        parser.add_argument("directory")
        self.args = parser.parse_args()
        self.folder_path = self.args.directory
        self.create_folder()

    def create_folder(self):
        os.makedirs(self.folder_path, exist_ok=True)

    def main(self):
        while True:
            user_url = input()
            if user_url == 'exit':
                return
            if user_url == 'back':
                self.back_site()
                continue
            if not user_url.startswith('https://'):
                user_url = 'https://' + user_url

            while not check_url(user_url):
                print('Invalid URL')
                user_url = input()
                if user_url == 'exit':
                    return

            response = requests.get(user_url)
            if response.status_code != 200:
                print('ERROR')
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                extracted_text = self.extract_text(soup)
                print(extracted_text)
                self.write_to_file(user_url.replace('https://', ""), extracted_text)

    def back_site(self):
        if self.my_stack:
            self.read_file(self.my_stack.pop())

    def write_to_file(self, url, content):
        file_name = url.split('.')[0]
        file_path = os.path.join(self.folder_path, file_name)
        with open(file_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(content)
            self.saved_files.append(file_name)

    def read_file(self, url):
        file_path = os.path.join(self.folder_path, url.split('.')[0])
        with open(file_path, 'r', encoding='utf-8') as f:
            print(f.read())

    def extract_text(self, soup):
        extracted_text = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']):
            if tag.name == 'a':
                extracted_text.append(Fore.BLUE + tag.get_text() + Style.RESET_ALL)
            else:
                extracted_text.append(tag.get_text())
        return '\n'.join(extracted_text)


browser = Browser()
browser.main()
