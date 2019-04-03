from bs4 import BeautifulSoup
import time
from selenium import webdriver
import requests
from user_agent import generate_user_agent

# CRAWLER_URL = 'https://community.smartthings.com/c/projects-stories'
CRAWLER_URL = 'https://community.smartthings.com/c/projects-stories?no_subcategories=false&page='
PAGE_COUNTER = 1
BASE_URL = 'https://community.smartthings.com'

## IMPLEMENT ID TAGGING SYSTEM TO DETERMINE WHEN TO STOP CRAWLING (ember43 for non crawler)
while PAGE_COUNTER != 113:
    #Selenium will load the page contents...
    profile = webdriver.FirefoxProfile()
    profile.set_preference('general.useragent.override', 'crawler')
    browser = webdriver.Firefox(profile)
    browser.get(CRAWLER_URL + str(PAGE_COUNTER))

    length_of_page = browser.execute_script('window.scrollTo(0, document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;')
    match = False
    page_count = 0
    max_page = 1
    while match == False:
        #last_count = length_of_page
        page_count += 1
        time.sleep(3)
        length_of_page = browser.execute_script('window.scrollTo(0, document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;')
        #if last_count == length_of_page:
        if page_count == max_page:
            match = True

    html_source = browser.page_source
    browser.close()
    # file = open('selenium_html.txt', 'w')
    # file.write(html_source)
    # print(source_data)

    # NOTE: Selenium works to load page data and output source, but now I need to find a way to feed the source to beautiful soup so that it can crawl for links.


    # headers = {"User-Agent": "Research User-Agent"}
    # page_response = requests.get(CRAWLER_URL, timeout=5, headers=headers)

    # content = BeautifulSoup(source_data, 'html.parser')
    # page = requests.get(CRAWLER_URL, timeout = 5)
    # if page.status_code == 200:
    #     print('URL: ', CRAWLER_URL, '\nRequest Successful!')
    #content = BeautifulSoup(page.content, 'html.parser')
    content = BeautifulSoup(html_source, 'html.parser')

# while content.find_all('div', {'class': 'topic-list'}) == True:
    project_urls = []
    page_links = content.find_all(class_="page-links")
    counter = 0
    for i in page_links:
        for m in i.contents:
            m = str(m)
            if ('(' not in m and ')' not in m and 'href' in m):
                s = BeautifulSoup(str(m),'lxml')
                link = s.find('a')
                appended_url = str(link.attrs['href'])
                page_string = '?page='
                final_url = BASE_URL + appended_url
                if page_string in final_url:
                    final_url = final_url.split(page_string)
                    final_url = final_url[0]
                    if final_url not in project_urls:
                        counter += 1
                        project_urls.append(final_url)
                        print(final_url)
                else:
                    project_urls.append(final_url)
                    print(final_url)
    #print(project_urls)
    print(counter)

    ## NEXT STEP: Crawl each page in the newly generated list of URLs and extract github links. Should be done by Wednesday.
    with open('output-urls.txt','a') as to_write:
        github_urls = []
        for k in project_urls: # TAB EVERYTHING BELOW THIS
            headers = {"crawler": "Research Crawler"}
            page_response = requests.get(k, timeout=5, headers=headers)

            page = requests.get(k, timeout = 5)
            #if page.status_code == 200:
            #print('URL: ', k, '\nRequest Successful!')
            content = BeautifulSoup(page.content, 'html.parser')

            for link in content.find_all('a', href=True):
                if 'github.com' in link['href']:
                    link_updated = link['href'].strip()
                    if(link_updated not in github_urls):
                        github_urls.append(link_updated)
                        print(link_updated)
                        to_write.write(link_updated+'\n')

    PAGE_COUNTER += 1
#Find app that extracts all website content (HTTrack)

# Get list of all the links --> print it out.
# Make it unique set(listName)

