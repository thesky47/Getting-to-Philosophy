"""Wikipedia Philosophy Game
 Clicking on the first link in the main text of an English Wikipedia article,
 and then repeating the process for subsequent articles,
 usually leads to the Philosophy article.
 In February 2016, this was true for 97% of all articles in Wikipedia.
 The remaining articles lead to an article without any outgoing wikilinks, to pages that do not exist, or get stuck in loops.
"""
from bs4 import BeautifulSoup
import requests

url_main = "https://en.wikipedia.org/" 

def trace(url):
    page = requests.get(url)    
    data = page.text
    soup = BeautifulSoup(data, 'lxml')

    div = soup.find('div', id="mw-content-text")
    paras = div.find_all('p') #All link in text are inside <p>, thus code skips links in tables etc.
    flag = False # used to break loop when code finds 1st link
    for para in paras: #some <p> don't have <a>
        for link in para.find_all('a'):
            if type(link) == type(para):
                href = link.get('href')
                if exclude(href):
                    continue
                the_link = href
                title = link.get('title')
                flag = True
                break
        if flag:
            break

    return the_link, title

def exclude(item):
    #excludes in page ref and ref to img etc.
    return '#' in item or ':' in item or '.' in item

"""Main code"""        
counter = 0
message = """Wikipedia Philosophy Game

Welcome, It is claimed that if click first link on 
any wikipedia page, it will lead you to philosophy page
This program takes a wikipedia page link and traverse first link
till Philosophy page 
"""
print(message)
url = input('Enter a Wikipedia page link:')

if not bool(url):
    url ="https://en.wikipedia.org/wiki/Fact" 

while True:
    counter += 1
    first, title = trace(url)
    print(title)
    if title == 'Philosophy':
        print('Total jumps needed to reach Philosophy:', counter)
        break
    url = url_main + first
