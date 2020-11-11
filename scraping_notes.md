As in the example before, we are importing the urlopen library and calling html.read()in order to get the HTML content of the page. This HTML content is then transformed into a BeautifulSoup object, with the following structure:
```
- html→ <html><head>...</head><body>...</body></html>
    — head→ <head><title>A Useful Page<title></head>
        — title→ <title>A Useful Page</title>
    — body→ <body><h1>An Int...</h1><div>Lorem ip...</div></body>
        — h1→ <h1>An Interesting Title</h1>
        — div→ <div>Lorem Ipsum dolor...</div>
```

Let’s take a look at the first line of our scraper, after the import statements, and figure out how to handle any exceptions this might throw:
```
html = urlopen("http://www.pythonscraping.com/pages/page1.html")
```

There are two main things that can go wrong in this line:
+ The page is not found on the server (or there was some error in retrieving it)
+ The server is not found

+ In the first situation, an HTTP error will be returned. This HTTP error may be “404 Page Not Found,” “500 Internal Server Error”, etc.
+ In all of these cases, the urlopen function will throw the generic exception “HTTPError"

We can handle this exception in the following way:
```
try:
    html = urlopen("http://www.pythonscraping.com/pages/page1.html")
except HTTPError as e:
    print(e)
    #return null, break, or do some other "Plan B"
else:
    #program continues. Note: If you return or break in the
    #exception catch, you do not need to use the "else" statement
```
+ If an HTTP error code is returned, the program now prints the error and does not execute the rest of the program under the else statement.

+ If the server is not found at all (if, say, http://www.pythonscraping.com was down, or the URL was mistyped), urlopen returns a None object. This object is analogous to null in other programming languages.

We can add a check to see if the returned html is None:
```
if html is None:
    print("URL is not found")
else:
    #program continues
```

+ Of course, if the page is retrieved successfully from the server, there is still the issue of the content on the page not quite being what we expected.
+ Every time you access a tag in a BeautifulSoup object, it’s smart to add a check to make sure the tag actually exists.
+ If you attempt to access a tag that does not exist, BeautifulSoup will return a None object. The problem is, attempting to access a tag on a None object itself will result in an AttributeError being thrown.

The easiest way to avoid this is to explicitly check for both situations:
```
try:
    badContent = bsObj.nonExistingTag.anotherTag
except AttributeError as e:
    print("Tag was not found")
else:
    if badContent == None:
        print ("Tag was not found")
    else:
        print(badContent)
```

This code, for example, is our same scraper written in a slightly different way:
```
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title

title = getTitle("http://www.pythonscraping.com/pages/page1.html")

if title == None:
    print("Title could not be found")
else:
    print(title)
```

+ In this example, we’re creating a function getTitle, which returns either the title of the page, or a None object if there was some problem with retrieving it.
+ Inside getTitle, we check for an HTTPError, as in the previous example, and also encapsulate two of the BeautifulSoup lines inside one try statement.
+ An AttributeError might be thrown from either of these lines (if the server did not exist, html would be a None object, and html.read() would throw an AttributeError).
+ We could, in fact, encompass as many lines as we wanted inside one try statement, or call another function entirely, which can throw an AttributeError at any point.

> When writing scrapers, it’s important to think about the overall pattern of your code in order to handle exceptions and make it readable at the same time. You’ll also likely want to heavily reuse code.
+ Having generic functions such as getSiteHTML and getTitle(complete with thorough exception handling) makes it easy to quickly and reliably scrape the web.

# ---------------------------------------------------------------------------------------------------------- #

In this section, we’ll begin a project that will become a “Six Degrees of Wikipedia" solution finder. That is, we’ll be able to take the Eric Idle pageand find the fewest number of link clicks that will take us to the Kevin Bacon page.

You should already know how to write a Python script that retrieves an arbitrary
Wikipedia page and produces a list of links on that page:
```
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)

for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])
```

If you look at the list of links produced, you’ll notice that all the articles you’d expect are there: “Apollo 13,” “Philadelphia,” “Primetime Emmy Award,” and so on. However, there are some things that we don’t want as well In fact, Wikipedia is full of sidebar, footer, and header links that appear on every page, along with links to the category pages, talk pages, and other pages that do not contain different articles

Recently a friend of mine, while working on a similar Wikipedia-scraping project, mentioned he had written a very large filtering function, with over 100 lines of code, in order to determine whether an internal Wikipedia link was an article page or not. Unfortunately, he had not spent much time up front trying to find patterns between “article links” and “other links,” or he might have discovered the trick.

If you examine he links that point to article pages (as opposed to other internal pages), they all have three things in common:
+ They reside within the divwith the idset to bodyContent
+ The URLs do not contain semicolons
+ The URLs begin with /wiki/

We can use these rules to revise the code slightly to retrieve only the desired article links:
```
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)

for link in bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])
```

Of course, having a script that finds all article links in one, hardcoded Wikipedia arti‐cle, while interesting, is fairly useless in practice. We need to be able to take this code and transform it into something more like the following:
+ A single function, getLinks, that takes in a Wikipedia article URL of the form  /wiki/<Article_Name> and returns a list of all linked article URLs in the same form.
+ A main function that calls getLinks with some starting article, chooses a random article link from the returned list, and calls getLinks again, until we stop the program or until there are no article links found on the new page.

Here is the complete code that accomplishes this:
```
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)
```

The first thing the program does, after importing the needed libraries, is set the random number generator seed with the current system time. This practically ensures a new and interesting random path through Wikipedia articles every time the program is run.

Creating a basic script that crawls Wikipedia, looks for revision history pages, and then looks for IP addresses on those revision history pages isn’t difficult. Using modified code from Chapter 3, the following script does just that:
```
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)

    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

def getHistoryIPs(pageUrl):
    #Format of revision history pages is:
    #http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    pageUrl = pageUrl.replace("/wiki/", "")

    historyUrl = "http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
    print("history url is: "+historyUrl)

    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html)

    #finds only the links with class "mw-anonuserlink" which has IP addresses
    #instead of usernames
    ipAddresses = bsObj.findAll("a", {"class":"mw-anonuserlink"})
    addressList = set()

    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    return addressList

links = getLinks("/wiki/Python_(programming_language)")

while(len(links) > 0):
    for link in links:
        print("-------------------")
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            print(historyIP)

newLink = links[random.randint(0, len(links)-1)].attrs["href"]
links = getLinks(newLink)
```

## Collecting Data Across an Entire Site

Of course, web crawlers would be fairly boring if all they did was hop from one pageto the other. In order to make them useful, we need to be able to do something on thepage while we’re there. Let’s look at how to build a scraper that collects the title, the first paragraph of content, and the link to edit the page (if available).

As always, the first step to determine how best to do this is to look at a few pages from the site and determine a pattern. By looking at a handful of Wikipedia pages both articles and non-article pages such as the privacy policy page, the following things should be clear:
+ All titles (on all pages, regardless of their status as an article page, an edit history page, or any other page) have titles under h1→spantags, and these are the only h1tags on the page.
+ As mentioned before, all body text lives under the div#bodyContent tag. However, if we want to get more specific and access just the first paragraph of text, we might be better off using div#mw-content-text→p (selecting the first paragraph tag only).
+ This is true for all content pages except file pages (for example: https://en.wikipedia.org/wiki/File:Orbit_of_274301_Wikipedia.svg), which do not have sections of content text.
+ Edit links occur only on article pages. If they occur, they will be found in the li#ca-edittag, under li#ca-edit→ span→ a.


# ------------------------------------------------------------- #
# Handling Logins and Cookies

So far, we’ve mostly discussed forms that allow you submit information to a site or let you to view needed information on the page immediately after the form. How is this different from a login form, which lets you exist in a permanent “logged in” state throughout your visit to the site?

Most modern websites use cookies to keep track of who is logged in and who is not. Once a site authenticates your login credentials a it stores in your browser a cookie, which usually contains a server-generated token, timeout, and tracking information.
The site then uses this cookie as a sort of proof of authentication, which is shown to each page you visit during your time on the site. Before the widespread use of cookies in the mid-90s, keeping users securely authenticated and tracking them was a huge problem for websites.

Although cookies are a great solution for web developers, they can be problematic for web scrapers. You can submit a login form all day long, but if you don’t keep track of the cookie the form sends back to you afterward, the next page you visit will act as though you’ve never logged in at all.

+ I’ve created a simple login form at http://pythonscraping.com/pages/cookies/login.html (the username can be anything, but the password must be “password”).
+ This form is processed at http://pythonscraping.com/pages/cookies/welcome.php, and contains a link to the “main site” page, http://pythonscraping.com/pages/cookies/profile.php.

+ If you attempt to access the welcome page or the profile page without logging in first,you’ll get an error message and instructions to log in first before continuing.
+ On the profile page, a check is done on your browser’s cookies to see whether its cookie was set on the login page.

Keeping track of cookies is easy with the Requests library:
```
import requests

params = {'username': 'Ryan', 'password': 'password'}

r = requests.post("http://pythonscraping.com/pages/cookies/welcome.php", params)

print("Cookie is set to:")
print(r.cookies.get_dict())
print("-----------")
print("Going to profile page...")

r = requests.get("http://pythonscraping.com/pages/cookies/profile.php",cookies=r.cookies)
print(r.text)
```
+ Here I am sending the login parameters to the welcome page, which acts as the processor for the login form.
+ I retrieve the cookies from the results of the last request, print the result for verification, and then send them to the profile page by setting the cookies argument.

+ This works well for simple situations, but what if you’re dealing with a more complicated site that frequently modifies cookies without warning, or if you’d rather not even think about the cookies to begin with?
+ The Requests session function works perfectly in this case:
```
import requests

session = requests.Session()

params = {'username': 'username', 'password': 'password'}

s = session.post("http://pythonscraping.com/pages/cookies/welcome.php", params)

print("Cookie is set to:")
print(s.cookies.get_dict())
print("-----------")
print("Going to profile page...")

s = session.get("http://pythonscraping.com/pages/cookies/profile.php")
print(s.text)
```
In this case, the session object (retrieved by calling requests.Session()) keeps track of session information, such as cookies, headers, and even information about protocols you might be running on top of HTTP, such as HTTPAdapters.
