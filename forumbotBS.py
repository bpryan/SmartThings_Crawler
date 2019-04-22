from bs4 import BeautifulSoup
import time
from selenium import webdriver
import requests
import re
from user_agent import generate_user_agent

class Crawler:

    def __init__(self):
        self.CRAWLER_URL = 'https://community.smartthings.com/c/projects-stories?no_subcategories=false&page='
        self.PAGE_COUNTER = 1
        self.BASE_URL = 'https://community.smartthings.com'

    def html_grab(self):
        #Selenium will load the page contents...
        print("--Now fetching page " + str(self.PAGE_COUNTER) + "--")
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', 'crawler')
        
        browser = webdriver.Firefox(profile)
        browser.get(self.CRAWLER_URL + str(self.PAGE_COUNTER))

        html_source = browser.page_source
        browser.close()

        content = BeautifulSoup(html_source, 'html.parser')

        # if content.find_all('table', {'class': 'topic-list'}):
        if content.findAll('tr'):
            if content.findAll('td'):
                return self.scrape_project_urls(content)
            else:
                return '--End of List Reached.--'

    def scrape_project_urls(self, content):
        project_urls = []
        for link in content.findAll('a', attrs={'href': re.compile(self.BASE_URL + '/t/')}):
            project_urls.append(link.get('href'))
        # print(project_urls)  # TEST CODE
        counter = 0
        for i in project_urls:
            counter += 1
        print("--" + str(counter) + " projects found on page " + str(self.PAGE_COUNTER) + "--")
        return self.scrape_github_urls(project_urls)
        

    def scrape_github_urls(self, urls):
        with open('output-urls.txt','a') as to_write:
            github_urls = []
            for k in urls: 
                headers = {"crawler": "Research Crawler"}
                page_response = requests.get(k, timeout=5, headers=headers)
                page = requests.get(k, timeout = 5)
                content = BeautifulSoup(page.content, 'html.parser')

                for link in content.find_all('a', href=True):
                    if 'github.com' in link['href']:
                        link_updated = link['href'].strip()
                        if(link_updated not in github_urls):
                            github_urls.append(link_updated)
                            print(link_updated)
                            to_write.write(link_updated+'\n')
        self.PAGE_COUNTER += 1
        self.html_grab()

forumbot = Crawler()
print(forumbot.html_grab())
