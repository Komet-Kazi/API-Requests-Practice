"""Scrape metadata from target URL."""
import requests
from bs4 import BeautifulSoup
from collections import Counter
import pprint
from PIL import Image
from io import BytesIO
import lxml
from urllib.parse import urljoin


def scrape_page_metadata(url):
    """Scrape target URL for metadata."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }

    pp = pprint.PrettyPrinter(indent=4)

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    metadata = {
        'title': get_title(soup),
        'description': get_description(soup),
        'image': get_image(soup),
        'img': display_picture(get_image(soup)),
        'favicon': get_favicon(soup, url),
        'sitename': get_site_name(soup, url),
        'color': get_theme_color(soup),
        'url': url,
        'links': get_all_site_links(soup, url),
        'words': get_most_used_words(soup)
    }

    pp.pprint(metadata)
    return metadata


def get_title(soup):
    """Scrape page title."""
    title = None

    if soup.title.string:
        title = soup.title.string
    elif soup.find("meta", property="og:title"):
        title = soup.find("meta", property="og:title").get('content')
    elif soup.find("meta", property="twitter:title"):
        title = soup.find("meta", property="twitter:title").get('content')
    elif soup.find("h1"):
        title = soup.find("h1").string
    return title


def get_description(soup):
    """Scrape page description."""
    description = None

    if soup.find("meta", property="description"):
        description = soup.find("meta", property="description").get('content')
    elif soup.find("meta", property="og:description"):
        description = soup.find(
            "meta", property="og:description").get('content')
    elif soup.find("meta", property="twitter:description"):
        description = soup.find(
            "meta", property="twitter:description").get('content')
    elif soup.find("p"):
        description = soup.find("p").contents
    return description


def get_image(soup):
    """Scrape share image."""
    image = None

    if soup.find("meta", property="image"):
        image = soup.find("meta", property="image").get('content')
    elif soup.find("meta", property="og:image"):
        image = soup.find("meta", property="og:image").get('content')
    elif soup.find("meta", property="twitter:image"):
        image = soup.find("meta", property="twitter:image").get('content')
    elif soup.find("img", src=True):
        image = soup.find_all("img").get('src')
    return image


def get_site_name(soup, url):
    """Scrape site name."""
    if soup.find("meta", property="og:site_name"):
        site_name = soup.find("meta", property="og:site_name").get('content')
    elif soup.find("meta", property='twitter:title'):
        site_name = soup.find("meta", property="twitter:title").get('content')
    else:
        site_name = url.split('//')[1]
        return site_name.split('/')[0].rsplit('.')[1].capitalize()
    return site_name


def get_favicon(soup, url):
    """Scrape favicon."""
    if soup.find("link", attrs={"rel": "icon"}):
        favicon = soup.find("link", attrs={"rel": "icon"}).get('href')
    elif soup.find("link", attrs={"rel": "shortcut icon"}):
        favicon = soup.find("link", attrs={"rel": "shortcut icon"}).get('href')
    else:
        favicon = f'{url.rstrip("/")}/favicon.ico'
    return favicon


def display_picture(image):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }
    response = requests.get(image, headers=headers)
    img = Image.open(BytesIO(response.content))
    return img


def get_theme_color(soup):
    """Scrape brand color."""
    if soup.find("meta", property="theme-color"):
        color = soup.find("meta", property="theme-color").get('content')
        return color
    return None


def get_all_site_links(soup, url):
    """Scrape all anchors on page."""
    page_links = {}

    if len(soup.body.find_all("a")) >= 1:
        for anchor in soup.body.find_all("a"):
            # urls with no length are discarded
            if len(anchor.text) >= 1 and page_links.get(anchor.text) is None:
                # resolve relational Url to absolute Url
                try:
                    linkBuilder = urljoin(url, anchor.get('href'))
                    page_links[anchor.text] = linkBuilder
                except UnicodeError:
                    continue
            else:
                continue
    else:
        return page_links
    return page_links

def get_most_used_words(soup):
    wordlist = []

    for each_text in soup.findAll('div', {'class': 'entry-content'}):
        content = each_text.text

        # use split() to break the sentence into
        # words and convert them into lowercase
        words = content.lower().split()

        for each_word in words:
            wordlist.append(each_word)

    clean_list = []

    for word in wordlist:
        symbols = '!@#$%^&*()_-+={[}]|\;:"<>?/., '

        for i in range(0, len(symbols)):
            word = word.replace(symbols[i], '')

        if len(word) > 0:
            clean_list.append(word)

    word_count = {}

    for word in clean_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    c = Counter(word_count)
    # returns the most occurring elements
    top = c.most_common(10)
    return top

if __name__ == "__main__":
    scrape_page_metadata(r'https://www.geeksforgeeks.org/python-programming-language/')
