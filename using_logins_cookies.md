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
