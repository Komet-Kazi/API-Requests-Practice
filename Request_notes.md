# Introduction to HTTP request

+ Whenever our Web browser tries communicating with a Web server, it is done by using the Hypertext Transfer Protocol(HTTP) which functions as a request-response protocol.

> We can grasp the important parts of the request after looking at the following example:
```
* Connected to google.com (74.125.236.35) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.35.0
> Host: google.com
> Accept: */*
>
< HTTP/1.1 302 Found
< Cache-Control: private
< Content-Type: text/html; charset=UTF-
< Location: http://www.google.co.in/?gf
qMUVKLCIa3M8gewuoCYBQ
< Content-Length: 261
< Date: Sat, 13 Sep 2014 20:07:26 GMT
* Server GFE/2.0 is not blacklisted
< Server: GFE/2.0
< Alternate-Protocol: 80:quic,p=0.002
```

## Parts of the HTTP request:
+ Method: The GET / http /1.1in the preceding example, is the HTTP method which is case sensitive. Here are some of the HTTP request methods:
    + GET: This fetches informationfrom the given server using the given URI.
    + HEAD: The functionality of this is similar to GET but the difference is, it delivers only the status line and header section.
    + POST: This can submit data to the server that we wish to process.
    + PUT: This creates or overwrites all the current representations of the target resource, when we intend to create a new URL.
    + DELETE: This removes all the resources that are described by the given Request-URI.
    + OPTIONS: This specifies the communication options for a request/response cycle. It lets the client to mention different options associated with the resource.
+ Request URI: Uniform Resource Identifier (URI) has the ability to recognize the name of theresource. In the previous example, the hostname is the Request-URI.
+ Request Header fields: If we want to add more information about the request, we can use the requests header fields. Some of the request-headers values are:
    + Accept-Charset: This is used to indicate the character sets that are acceptable for the response.
    + Authorization: This contains the value of the credentials which has the authentication information of the user agent.
    + Host: This identifies the Internet host and port number of the resource that has been requested, using the original URI given by the user.
    + User-agent: It accommodatesinformation about the user agent that originates the request. This can be used for statistical purposes such as tracing the protocol violations.

## Making a simple request
```
>>> import requests
>>> r = requests.get('http://google.com')
```

> The response object 'r' contains a lot of information about the response, such as header information, content, type of encoding, status code, URL information and many more sophisticated details.

+ We can use all the HTTP request methods like GET(shown above), POST, PUT, DELETE, HEAD with requests.
+ Now let us learn how to pass the parameters in URLs. We can add the parameters to a request using using the params keyword.

> The following is the syntax used for passing parameters:
```
parameters = {'key1': 'value1', 'key2': 'value2'}

r = requests.get('url', params=parameters)
```

> Let us get a GitHub user details by logging into GitHub, using requestsas shown in the following code:
```
>>> r = requests.get('https://api.github.com/user', auth=('myemailid.mail.com', 'password'))
>>> r.status_code
200
>>> r.url
u'https://api.github.com/user'
>>> r.request
<PreparedRequest [GET]>
```

+ We have used the 'auth' tuple which enables Basic/Digest/Custom Authentication to login to GitHub and get the user details.
+ The 'r.status_code' result indicates that we have successfully retrieved the user details.
+ 'r.url' accessed the URL.
+ 'r.request' returns the type of request.

## Response content

+ Response content is the information about the server's response that is delivered back to our console when we send a request.

+ While interacting with the web, it's necessary to decode the response of the server.
    + There are many cases in which we may have to deal with the raw, or JSON, or even binary response.
+ requests has the capability to automatically decode the content from the server.
    + requests makes informed guesses about the encoding of the response.
    + This basically happens taking the headers into consideration.
    + requests can smoothly decode many of the Unicode charsets.


+ 'r.content', access the response content in a raw string format.
+ 'r.text', the Requests library encodes the response (value of 'r.content') using 'r.encoding' and returns a new encoding string.
+ If the value of 'r.encoding' is None, Requests assumes the encoding type using 'r.apparent_encoding', which is provided by the 'chardet' library.

```
>>> import requests
>>> r = requests.get('https://google.com')

>>> r.content
'<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage", *args>'
>>> type(r.content)
<type 'str'>

>>> r.text
u'<!doctype html><html itemscope=""\ itemtype="http://schema.org/WebPage", lang="en-IN"><head><meta content="example">'
>>> type(r.text)
<type 'unicode'>
```

> In the preceding lines, we try to get the google homepage, using 'requests.get()' and assigning it to a variable 'r'.
> 'r' turns out to be a request object, and we can access the raw content using 'r.content' and the encoded response content with 'r.text'.

+ Find what encoding Requests is using and/or change the encoding with the property 'r.encoding'

> Example:
```
>>> r.encoding
'ISO-8859-1'

>>> r.encoding = 'utf-8'
```

+ Requests will use the latest value of 'r.encoding' that has been assigned.
    + So, if we change the encoding once it will use that value whenever we call 'r.text'.
    + If the value of 'r.encoding' is None, Requests will use the value of 'r.apparent_encoding'.
    + 'r.apparent_encoding' cannot be changed, Requests raises an 'AttributeError' as its value can't be altered.

> Example :
```
>>> r.encoding = None
>>> r.apparent_encoding
'ascii'
>>> r.apparent_encoding = 'ISO-8859-1'
Traceback (most recent call last):
File "<stdin>", line 1, in <module> AttributeError: can't set attribute
```

## Different types of request contents

+ Requests has the facility to deal with different types of Request contents like binary response content, JSON response content, and raw response content.
+ To give a clear picture on different types of response content, we listed the details.

> The examples used here are developed using Python 2.7.x.

### Custom headers
+ We can send custom headers with a request.
    + We just need to create a dictionary with our headers and pass the headers parameter in the 'get', or 'post' method.
    + The name of the header is the key and the value is the value of the pair.

> Let us pass an HTTP header to a request:
```
>>> import json

>>> url = 'https://api.github.com/some/endpoint'

>>> payload = {'some': 'data'}

>>> headers = {'Content-Type': 'application/json'}

>>> r = requests.post(url, data=json.dumps(payload), headers=headers)
```

> we provided the header: 'content-type' with value: 'application/json' as a parameter to the request. In the same way, we can send a request with a custom header.
    + Say, we have a necessity to send a request with an authorization header with a value as some token.
    + We can create a dictionary with key: 'Authorization', and value: 'a token'
> Example:
```
>>> url = 'some url'

>>> header = {'Authorization' : 'some token'}

>>> r.request.post(url, headers=headers)
```

### Sending form-encoded data
+ We can send form-encoded data like an HTML form using Requests.
+ A simple dictionary passed to the 'data' argument gets this done. The dictionary of data will turn as form-encoded automatically, when a request is made.
> Sending Form Example:
```
>>> payload = {'key1': 'value1', 'key2': 'value2'}

>>> r = request.post("some_url/post", data=payload)

>>> print(r.text)
{"form": {"key2": "value2","key1": "value1"}}
```

> ***Remember***: The previous example was specifically to send form-encoded data.

+ When dealing with data that is not form-encoded, we should send a string in the place of a dictionary.

### Posting multipart encoded files
> We tend to upload multipart data like images or files through **POST**.
+ We can achieve this in requests using a dictionary passed to the ***files*** parameter:
    + Dictionar Key:'name' and Value: 'file-like-objects'
    + Or Key:'name' and Value: ('filename', 'fileobj')

> Example :

```
{'name': file-like-objects}

OR

{'name': ('filename', fileobj)}
```

> The example is as follows:
```
>>> url = 'some api endpoint'

>>> files = {'file': open('plan.csv', 'rb')}
>>> r = requests.post(url, files=files)

>>> r.text
{"files":{"file": "<some data...>"}}
```

> In the former example, we didn't specify the content-type or headers.
> We have the capability to set the name for the file we are uploading:

```
>>> url = 'some url'

>>> files = {'file': ('plan.csv', open('plan.csv', 'rb'), 'application/csv', {'Expires': '0'})}
>>> r = requests.post(url, files)

>>> r.text
{"files": {"file": "<data...>"}}
```

> We can also send strings to be received as files in the following way:
```
>>> url = 'some url'

>>> files = {'file' : ('plan.csv', 'some, strings, to, send')}

>>> r.text
{"files": {"file": "some, strings, to, send"}}
```
## Looking up built-in response status codes

+ Status codes are helpful in letting us know the result of our sent request.
> To know about this, we can use 'status_code':
```
>>> r = requests.get('http://google.com')
>>> r.status_code
200
```
+ To make it much easier to deal with status_codes, Requests has got a built-in status code lookup object which serves as an easy reference.
+ We can compare the 'requests.codes.ok' with 'r.status_code':
    + If the result is True, then it's a 200 status code, and if it's False, it's not.
+ We can also compare the 'r.status.code' with 'requests.codes.ok', 'requests.code.all_good' to get the lookup work.

> Example:
```
>>> r = requests.get('http://google.com')
>>> r.status_code == requests.codes.ok
True
```

> Now, let's try checking with a URL that is non-existent:
```
>>> r = requests.get('http://google.com/404')
>>> r.status_code == requests.codes.ok
False
```

+ We have the ability to deal with the bad requests like, 4XX and 5XX type of errors, by raising the error codes.
+ This can be accomplished by using 'Response.raise_for_status()'.

> Let us try this by sending a bad request first:
```
>>> bad_request = requests.get('http://google.com/404')
>>> bad_request.status_code
404

>>>bad_request.raise_for_status()
---------------------------------------------------------------------------
HTTPError                                  Traceback(most recent call last)

----> bad_request..raise_for_status()
File "requests/models.py", in raise_for_status(self)
771
772 if http_error_msg:
--> 773 raise HTTPError(http_error_msg, response=self)
774
775 def close(self):

HTTPError: 404 Client Error: Not Found
```

> Now if we try a working URL, we get nothing in response, which is a sign of success:
```
>>> bad_request = requests.get('http://google.com')
>>> bad_request.status_code
200

>>> bad_request.raise_for_status()
>>>
```
## Viewing response headers
+ The server response header helps us to know about the software used by the origin server to handle the request.

> We can access the server response headers using r.headers:

```
>>> r = requests.get('http://google.com')

>>> r.headers
CaseInsensitiveDict({'alternate-protocol': '80:quic', 'x-xss-protection': '1; mode=block', 'transfer-encoding': 'chunked', 'set-cookie': 'PREF=ID=3c5de2786273fce1:FF=0:TM=1410378309:LM=1410378309:S=DirRRD4dRAxp2Q_3;
```

> Requests for Comments(RFC) 7230 says that HTTP header names are not case-sensitive.
> This gives us a capability to access the headers with both capital and lower-case letters.
```
>>> r.headers['Content-Type']
'text/html; charset=ISO-8859-1'

>>> r.headers.get('content-type')
'text/html; charset=ISO-8859-1'
```
## Accessing cookies with Requests

> We can access cookies from the response, if they exist:
```
>>> url = 'http://somewebsite/some/cookie/setting/url'
>>> r = requests.get(url)

>>> r.cookies['some_cookie_name']
'some_cookie_value'
```

> We can send our own cookies, as shown in the following example:
```
>>> url = 'http://httpbin.org/cookies'

>>> cookies = dict(cookies_are='working')
>>> r = requests.get(url, cookies=cookies)

>>> r.text
'{"cookies": {"cookies_are": "working"}}'
```

## Tracking redirection of the request using request history

+ Sometimes the URL that we are accessing may have been moved or it might get redirected to some other location. We can track them using Requests.
+ The response object's history property can be used to track the redirection.
+ Requests can accomplish location redirection with every verb except with HEAD.
+ The 'Response.history' list contains the objects of the Requests that were generated in order to complete the request.
```
>>> r = requests.get('http:google.com')

>>> r.url
u'http://www.google.co.in/?gfe_rd=cr&ei=rgMSVOjiFKnV8ge37YGgCA'
>>> r.status_code
200

>>> r.history
(<Response [302]>,)
```

> In the preceding example, when we tried sending a request to 'www.google.com', we got the 'r.history value' as 302 which means the URL has been redirected to some other location. The 'r.url' shows us the proof here, with the redirection URL.
> we can set the value of 'allow_redirects' to False if we are using POST, GET, PUT, PATCH, OPTIONS, or DELETE and/or we don't want Requests to handle redirections.

```
>>> r = requests.get('http://google.com', allow_redirects=False)

>>> r.url
u'http://google.com/'
>> r.status_code
302

>>> r.history
[ ]
```

> In the preceding example, we used the parameter 'allow_redirects' and set its value to False,
> This Resulted in the 'r.url' not being redirected and having a 302 status code in the URL and the 'r.history' as empty.

> If we are using the head to access the URL, we can facilitate redirection.
```
>>> r = requests.head('http://google.com', allow_redirects=True)

>>> r.url
u'http://www.google.co.in/?gfe_rd=cr&ei=RggSVMbIKajV8gfxzID4Ag'

>>> r.history
(<Response [302]>,)
```
> In this example, we tried accessing the URL with the 'head' method and the parameter 'allow_redirects' as True. This Resulted in the URL being redirected.

## Using timeout to keep productive usage in check
> Take a case in which we are trying to access a response which is taking too much time.

+ If we don't want to get the process moving forward and give out an exception if it exceeds a specific amount of time, we can use the parameter 'timeout'.
    + When we use the timeout parameter, we are telling Requests not to wait for a response after some specific time period.
    + If we use timeout, it's not equivalent to defining a time limit on the whole response download.
    + It's a good practice to raise an exception if no bytes have been acknowledged on the underlying socket for the stated timeout in seconds

```
>>> requests.get('http://google.com', timeout=0.03)
---------------------------------------------------------------------------
Timeout                                 Traceback (most recent call last)
Timeout: HTTPConnectionPool(host='google.com', port=80):
Read timed\ out.(read timeout=0.03)
```

> In the previous  example we have specified the 'timeout' value as 0.03
> The timeout has been exceeded while retrieving the response and so it resulted us the 'timeoutexception'.

+ The timeout may occur in two different cases:
    + The request getting timed out while attempting to connect to the server that is in a remote place.
    + The request getting timed out if the server did not send the whole response in the allocated time period.


## Errors and exceptions
+ Different types of errors and exceptions will be raised when something goes wrong in the process of sending a request and getting back a response.

+ Some of them are as follows:
    + HTTPError: When thereare invalid HTTP responses, Requests will raise an HTTPErrorexception
    + ConnectionError: If thereis a network problem, such as refused connection and DNS failure, Requests will raise a ConnectionErrorexception
    + Timeout: If the request getstimed out, this exception will be raised
    + TooManyRedirects: If the requestsurpasses the configured number of maximum redirections, this type of exception is raised.
    + Other types of exception that come in to the picture are: Missing schema Exception, InvalidURL, ChunkedEncodingError, and ContentDecodingError and so on.

## Summary
In this chapter, we covered a few basic topics. We learned why:
+ Requests is better than urllib2
+ how to make a simple request
+ different types of response contents
+ adding custom headers to our Requests
+ dealing with form encoded data
+ using the status code lookups
+ locating request redirection location and about timeouts.

> In the next chapter we will learn the advanced concepts in Requests in depth which will help us to use the Requests library flexibly according to the requirements.

# ------------------------------------------------------------------------------------------------------------ #

> In this chapter, we are going to deal with advanced topics in the Requests module. There are many more features in the Requests module that makes interaction with the web a cakewalk.

+ In a nutshell, we will cover the following topics:
    + Persisting parameters across Requests using Session objects
    + Revealing the structure of Request and response
    + Using prepared Requests
    + Verifying SSL certificate with Requests
    + Body Content Workflow
    + Using generator for sending chunk encoded Requests
    + Getting the Request method arguments with event hooks
    + Iterating over streaming API
    + Self-describing the APIs with link headers
    + Transport Adapter

## Persisting parameters across Requests using Session objects

> The Requests module contains a session object, which has the capability to persist settings across the Requests.
> Using this session object, we can persist cookies, we can create prepared Requests, we can use the keep-alive feature and do many more things.
> The Session object contains all the methods of Requests API such as GET, POST, PUT, DELETE and so on.

> Let us use the session method to get the resource
```
>>> import requests
>>> session = requests.Session()
>>> response = requests.get("https://google.co.in", cookies={"new-cookieidentifier": "1234abcd"})
```

> In the preceding example, we created a Session object with Requests and used it's GET method is used to access a web resource.

> The cookie value which we had set in the previous example will be accessible using 'response.request.headers'
```
>>> response.request.headers
CaseInsensitiveDict({'Cookie': 'new-cookie-identifier=1234abcd', 'AcceptEncoding': 'gzip, deflate, compress', 'Accept': '*/*', 'User-Agent': 'python-requests/2.2.1 CPython/2.7.5+ Linux/3.13.0-43-generic'})

>>> response.request.headers['Cookie']
'new-cookie-identifier=1234abcd'
```

+ With a Session object, we can specify default values of the properties, to be sent to the server using GET, POST, PUT and so on.

> We can achieve this by specifying the values to the properties like headers, auth and so on, on a Session object.
```
>>> session.params = {"key1": "value", "key2": "value2"}

>>> session.auth = ('username', 'password')
>>> session.headers.update({'foo': 'bar'})
```

+ In the preceding example, we have set some default values to the properties: params, auth, and headers using the Session object.

> We can override them in the subsequent request, as shown in the following example, if we want to:
```
>>> session.get('http://mysite.com/new/url', headers={'foo': 'new-bar'})
```
## Revealing the structure of a request and response
+ A Requests object is the one which is created by the user when he/she tries to interact with a web resource.
+ It will be sent as a prepared request to the server and does contain some parameters which are optional.

+ Parameters:
    + Method: This is theHTTP method to be used to interact with the web service. For example: GET, POST, PUT.
    + URL: The web address to which the request needs to be sent.
    + headers: A dictionary of headers to be sent in the request.
    + files: This can be used while dealing with the multipart upload. It's the dictionary of files, with key as file name and value as file object.
    + data: This is the body to be attached to the request.json. There are two cases that come in to the picture here:
        + If json is provided, content-type in the header is changed to application/json and at this point, json acts as a body to the request.
        + In the second case, if both json and data are provided together, data is silently ignored.
    + params: A dictionaryof URL parameters to append to the URL.
    + auth: This is used when weneed to specify the authentication to the request. It's a tuple containing username and password.
    + cookies: A dictionaryor a cookie jar of cookies which can be added to the request.
    + hooks: A dictionary of callbackhooks.

> A Response object contains the response of the server to a HTTP request. It is generated once Requests gets a response back from the server.

+ It contains all of the information returned by the server and also stores the Request object we created originally.
+ Whenever we make a call to a server using the requests, two major transactions are taking place in this context which are listed as follows:
    + We are constructing a Request object, which will be sent out to the server to request a resource
    + A Response object is generated by the requests module

> Now, let us look at an example of getting a resource from Python's official site.
```
>>> response = requests.get('https://python.org')
```

+ In the preceding line of code, a requests object gets constructed and will be sent to 'https://python.org'.
+ Thus, obtained Requests object will be stored in the 'response.request' variable.

> We can access the headers of the Request object, which was sent off to the server in the following way:
```
>>> response.request.headers
CaseInsensitiveDict({'Accept-Encoding': 'gzip, deflate, compress', 'Accept': '*/*', 'User-Agent': 'python-requests/2.2.1 CPython/2.7.5+ Linux/3.13.0-43-generic'})
```

> The headers returned by the server can be accessed with its 'headers' attribute as shown in the following example:

```
>>> response.headers
CaseInsensitiveDict({'content-length': '45950', 'via': '1.1 varnish', 'x-cache': 'HIT', 'accept-ranges': 'bytes', 'strict-transport-security': 'max-age=63072000; includeSubDomains', 'vary': 'Cookie', 'server': 'nginx', 'age': '557','content-type': 'text/html; charset=utf-8', 'public-key-pins': 'max-age=600; includeSubDomains; ..)
```

+ The response object contains different attributes like:
    + _content
    + status_code
    + headers
    + url
    + history
    + encoding
    + reason
    + cookies
    + elapsed
    + request

```
>>> response.status_code
200

>>> response.url
u'https://www.python.org/'

>>> response.elapsed
datetime.timedelta(0, 1, 904954)

>>> response.reason
'OK'
```

## Using prepared Requests

+ Every request we send to the server turns to be a PreparedRequest by default. The request attribute of the Response object which is received from an API call or a session call is actually the PreparedRequest that was used.
+ There might be cases in which we need to send a request with the extra step of adding a different parameter. Parameters can be cookies, files, auth, timeout and so on.
+ We can handle this extra step efficiently by using the combination of sessions and prepared requests.

> Let us look at an example:
```
>>> from requests import Request, Session
>>> header = {}
>>> request = Request('get', 'some_url', headers=header)
```

+ We are trying to send a get request with a header in the previous example.
+ Now, take an instance where we are planning to send the request with the same method, URL, and headers, but we want to add some more parameters to it.
+ We can use the session method to receive complete session level state to access the parameters of the initial sent request.

> This can be done by using the session object.
```
>>> from requests import Request, Session
>>> session = Session()
>>> request1 = Request('GET', 'some_url', headers=header)
```

> Now, let us prepare a request using the session object to get the values of the session level state:
```
>>> prepare = session.prepare_request(request1)
```

> We can send the request object request with more parameters now, as follows:
```
>>> response = session.send(prepare, stream=True, verify=True)
200
```

+ Voila! Huge time saving!

+ In the previous example, the prepare_request method was used.
    + The prepare method prepares the complete request with the supplied parameters.
+ There are also some other methods which are used to create individual properties like:
    + prepare_auth
    + prepare_body
    + prepare_cookies
    + prepare_headers
    + prepare_hooks
    + prepare_method
    + prepare_url

## Verifying an SSL certificate with Requests
> Requests provides the facilityto verify an SSL certificate for HTTPS requests. We can use the verify argument to check whether the host's SSL certificate is verified or not. Let us consider a website which has got no SSL certificate. We shall send a GET request with the argument verify to it.

> The syntax to send the request is as follows:
```
requests.get('no ssl certificate site', verify=True)
```

> If the website doesn't have an SSL certificate, it will result an error similar to the following:
```
requests.exceptions.ConnectionError: ('Connection aborted.', error(111, 'Connection refused'))
```

> Let us verify the SSL certificate for a website which is certified. Consider the following example:
```
>>> requests.get('https://python.org', verify=True)
<Response [200]>
```

+ In the preceding example, the result was 200,as the mentioned website is a SSL certified one.
+ If we do not want to verify the SSL certificate with a request, then we can put the argument verify=False.
+ By default, the value of verify will turn to True.

## Body Content Workflow
> Take an instance where a continuous stream of data is being downloaded when we make a request. In this situation, the client has to listen to the server continuously until it receives the complete data.
> Consider the case of accessing the content from the response first and the worry about the body next.
> In the above two situations, we can use the parameter stream.

```
>>> requests.get("https://pypi.python.org/packages/source/F/Flask/Flask-0.10.1.tar.gz", stream=True)
```

+ If we make a request with the parameter 'stream' set as True, the connection remains open and only the headers of the response will be downloaded.
+ This gives us the capability to fetch the content whenever we need by specifying the conditions like the number of bytes of data.

> The syntax is as follows:
```
if int(request.headers['content_length']) < TOO_LONG:
content = r.content
```

+ By setting the parameter 'stream' to True and by accessing the response as a file-like object that is 'response.raw',

+ If we use the method 'iter_content', we can iterate over 'response.data'. This will avoid reading of larger responses at once.

> The syntax is as follows:
```
iter_content(chunk_size=size in bytes, decode_unicode=False)
```


+ In the same way, we can iterate through the content using 'iter_lines' method which will iterate over the response data one line at a time.

> The syntax is as follows:
```
iter_lines(chunk_size = size in bytes, decode_unicode=None, delimitter=None)
```

## The Keep-alive facility
+ As the urllib3 supports the reuse of the same socket connection for multiple requests, we can send many requests with one socket and receive the responses using the keep-alive feature in the Requests library.
+ Within a session, it turns to be automatic. Every request made within a session automatically uses the appropriate connection by default.
+ The connection that is being used will be released after all the data from the body is read.

## Streaming uploads
+ A file-like object which is of massive size can be streamed and uploaded using the Requests library.
+ All we need to do is to supply the contents of the stream as a value to the data attribute in the request call as shown in the following lines.
> The syntax is as follows:
```
with open('massive-body', 'rb') as file:
    requests.post('http://example.com/some/stream/url',data=file)
```

## Iterating over streaming APIs
+ Streaming API tends to keep the request open allowing us to collect the stream data in real time.
+ While dealing with a continuous stream of data, to ensure that none of the messages being missed from it we can take the help of iter_lines() in Requests.
+ iter_lines() iterates over the response data line by line. This can be achieved by setting the parameter stream as True while sending the request
```
>>> import json
>>> import requests

>>> r = requests.get('http://httpbin.org/stream/4', stream=True)

>>> for line in r.iter_lines():
        if line:
            print(json.loads(line))
```

+ In the preceding example, the response contains a stream of data.
+ Using iter_lines(), We tried to print the data by iterating through every line.

## Encodings
> As specified in the HTTP protocol (RFC 7230), applications can request the server to return the HTTP responses in an encoded format.
> The process of encoding turns the response content into an understandable format which makes it easy to access it.
> When the HTTP header fails to return the type of encoding, Requests will try to assume the encoding with the help of chardet.

> If we access the response headers of a request, it does contain the keys of content-type.
> Let us look at a response header's content-type:
```
>>> re = requests.get('http://google.com')
>>> re.headers['content-type']
'text/html; charset=ISO-8859-1'
```

+ In the preceding example the content type contains 'text/html; charset=ISO-8859-1'.
+ This happens when the Requests finds the charset value to be None and the 'content-type'value to be 'Text'.

+ It follows the protocol RFC 7230 to change the value of charset to ISO-8859-1 in this type of a situation. In case we are dealing with different types of encodings like 'utf-8', we can explicitly specify the encoding by setting the property to 'Response.encoding'

## HTTP verbs
> Requests support the usage of the full range of HTTP verbs which are defined in the following table. To most ofthe supported verbs, 'url' is the only argument that must be passed while using them.

+ GET
    + GET method requests a representation of the specified resource.
    + Apart from retrieving the data, there will be no other effect of using this method.
    + Definition is given as requests.get(url, **kwargs)
+ POST
    + The POST verb is used for the creation of new resources.
    + The submitted data will be handled by the server to a specified resource.
    + Definition is given as requests.post(url, data=None, json=None, **kwargs)
+ PUT
    + This method uploads a representation of the specified URI.
    + If the URI is not pointing to any resource, the server can create a new object with the given data or it will modify the existing resource.
    + Definition is given as requests.put(url, data=None, **kwargs)
+ DELETE
    + This is pretty easy to understand. It is used to delete the specified resource.
    + Definition is given as requests.delete(url, **kwargs)
+ HEAD
    + This verb is useful for retrieving meta-information written in response headers without having to fetch the response body.
    + Definition is given as requests.head(url, **kwargs)
+ OPTIONS
    + OPTIONS is a HTTP method which returns the HTTP methods that the server supports for a specified URL.
    + Definition is given as requests.options(url, **kwargs)
+ PATCH
    + This method is used to apply partial modifications to a resource.
    + Definition is given as requests.patch(url, data=None, **kwargs)

## Self-describing the APIs with link headers
> Take a case of accessing a resource in which the information is accommodated in different pages. If we need to approach the next page of the resource, we can make use of the link headers.
> The link headers contain the meta data of the requested resource, that is the next page information in our case.
```
>>> url = "https://api.github.com/search/code?q=addClass+user:mozilla&page=1&per_page=4"

>>> response = requests.head(url=url)
>>> response.headers['link']
'<https://api.github.com/search/code?q=addClass+user%3Amozilla&page=2&per_page=4>; rel="next", <https://api.github.com/search/code?q=addClass+user%3Amozilla&page=250&per_page=4>; rel="last"
```

+ In the preceding example, we have specified in the URL that we want to access page number one and it should contain four records.
+ The Requests automatically parses the link headers and updates the information about the next page.
+ When we try to access the link header, it showed the output with the values of the page and the number of records per page.

## Transport Adapter
> It is used to provide an interface for Requests sessions to connect with HTTP and HTTPS. This will help us to mimic the web service to fit our needs.
> With the help of Transport Adapters, we can configure the request according to the HTTP service we opt to use.
+ Requests contains a Transport Adapter called HTTPAdapter included in it.
> Consider the following example:
```
>>> session = requests.Session()
>>> adapter = requests.adapters.HTTPAdapter(max_retries=6)
>>> session.mount("http://google.co.in", adapter)
```
+ In this example, we created a request session in which every request we make retries only six times, when the connection fails.

## Summary
In this chapter:
    + we learnt about creating sessions and using the session with different criteria.
    + We also looked deeply into HTTP verbs and using proxies.
    + We learnt about streaming requests, dealing with SSL certificate verifications and streaming responses.
    + We also got to know how to use prepared requests, link headers and chunk encoded requests.

> In the next chapter, we will learn about various types of authentication and ways to use them with Requests.

# ------------------------------------------------------------------------------------------------------------ #

# Authenticating with Requests
Requests supports diverse kinds of authentication procedures, and it is built in such a way that the method of authentication feels like a cakewalk.

+ In this chapter, we opt to throw light on various types of authentication procedures that are used by various tech giants for accessing the web resources.

+ We will cover the following topics:
    + Basic authentication
    + Digest authentication
    + Kerberos authentication
    + OAuth authentication
    + Custom authentication

## Basic authentication
Basic authentication is a popular, industry-standard scheme of authentication, which is specified in HTTP 1.0.

+ This method makes use of a user-ID and password submitted by the user to get authenticated.
+ The submitted user-ID and password are encoded using Base64 encoding standards and transmitted across HTTP.
+ The server gives access to the user only if the user-ID and the password are valid.

+ The following are the advantages of using basic authentication:

    + The main advantage of using this scheme is that it is supported by most of the web browsers and servers. Even though it is simple and straightforward, it does have some disadvantages. Though all the credentials are encoded and transferred in the requests, they are not encrypted which makes the process insecure. One way to overcome this problem is by using SSL support while initiating a secure session.

    + Secondly, the credentials persist on the server until the end of the browser session, which may lead to the seizure of the resources. And also, this authentication process is wide open to Cross Site Request Forgery(CSRF) attacks, as the browser automatically sends the credentials of the user in the subsequent requests.

+ The basic authentication flow contains two steps:
    1. If a requested resource needs authentication, the server returns http 401 response containing a WWW-Authenticateheader.
    2. If the user sends another request with the user ID and password in the Authorization header, the server processes the submitted credentials and gives the access.

## Using basic authentication with Requests
> We can use the requests module to send a request to undergo basic authentication very easily.

The process can be seen as follows:
```
>>> from requests.auth import HTTPBasicAuth
>>> requests.get('https://demo.example.com/resource/path', auth=HTTPBasicAuth('user-ID', 'password'))
```

+ In the preceding lines of code, we performed basic authentication by creating an HTTPBasicAuth object; then we passed it to the auth parameter, which will be submitted to the server.
+ If the submitted credentials gets authenticated successfully, the server returns a 200(Successful) response, otherwise, it will return a 401(Unauthorized) response.



## Digest authentication
#TODO

## Kerberos authentication
#TODO

## OAuth authentication
OAuth is an open standard authorization protocol, which allows client applications a secure delegated access to the user accounts on third party services such as Google, Twitter, GitHub and so on.
+ In this topic, we are going to introduce the two versions: OAuth 1.0 and OAuth 2.0

### OAuth 1.0
OAuth authentication protocol came up with an idea of mitigating the usage of passwords, replacing them with secure handshakes with API calls between the applications.
This was developed by a small group of web developers who are inspired by OpenID.

+ Here are the Key terms used in the process of OAuth authentication:
    + Consumer: The HTTP Client who can make authenticated requests
    + Service Provider: The HTTP Server, which deals with the requests of OAuth
    + User: A person who has the control over the protected resources on the HTTP Server
    + Consumer Key and Secret: Identifiers which have the capability to authenticate and authorize a request
    + Request Token and Secret: Credentials used to gain authorization from the user
    + Access Token and Secret: Credentials to get access to the protected resources of the user

+ Initially, the client application asks the service provider to grant a request token.
    + A user can be identified as an approved user by taking the credibility of the request token. It also helps in acquiring the access token with which the client application can access the service provider's resources.
+ In the second step, the service provider receives the request and issues request token, which will be sent back to the client application.
    + Later, the user gets redirected to the service provider's authorization page along with the request token received before as an argument.
+ In the next step, the user grants permission to use the consumer application.
    + Now, the service provider returns the user back to the client application, where the application accepts an authorized request token and gives back an access token.
    + Using the access token, the user will gain an access to the application.

## Using OAuth 1.0 authentication with Requests
> The requests_oauthlib is a an optional library for oauth which is not included in the Requests module. For this reason, we should install requests_oauthlib separately.

Let us take a look at the syntax:
```
>>> import requests
>>> from requests_oauthlib import OAuth1

>>> auth = OAuth1('<consumer key>', '<consumer secret>','<user oauth token>', '<user oauth token secret>')
>>> requests.get('https://demo.example.com/resource/path', auth=auth)
```

### OAuth 2.0
OAuth 2.0 is next in line to OAuth 1.0 which has been developed to overcome the drawbacks of its predecessor.
+ In modern days, OAuth 2.0 has been used vividly in almost all leading web services. Due to its ease of use with more security, it has attracted many people.
+ The beauty of OAuth 2.0 comes from its simplicity and its capability to provide specific authorization methods for different types of application like web, mobile and desktop.

Basically, there are four workflows available while using OAuth 2.0, which are also called grant types.

They are:
    1. Authorization code grant: This is basically used in web applications for the ease of authorization and secure resource delegation.
    2. Implicit grant: This flow is used to provide OAuth authorization in Mobile Applications.
    3. Resource owner password credentials grant: This type of grant is used for applications using trusted clients.
    4. Client credentials grant: This type of grant is used in machine to machine authentication. An in-depth explanation about grant types is out of the scope of this book.

+ OAuth 2.0 came up with capabilities which could overcome the concerns of OAuth 1.0. The process of using signatures to verify the credibility of API requests has been replaced by the use of SSL in OAuth 2.0.
+ It came up with the idea of supporting different types of flow for different environments ranging from web to mobile applications. Also, the concept of refresh tokens has been introduced to increase the security.

Let us take a look at the usage:
```
>>> from requests_oauthlib import OAuth2Session
>>> client = OAuth2Session('<client id>', token='token')
>>> resp = client.get('https://demo.example.com/resource/path')
```

# ------------------------------------------------------------------------------------------------------------ #

# Interacting with Social Media Using Requests
In this contemporary world, our lives are woven with a lot of interactions and collaborations with social media. The information that is available on the web is very valuable and it is being used by abundant resources.

For instance, the news that is trending in the world can be spotted easily from a Twitter hashtag and this can be achieved by interacting with the Twitter API. Using natural language processing, we can classify emotion of a person by grabbing the Facebook status of an account.

+ All this stuff can be accomplished easily with the help of Requests using the concerned APIs.
+ Requests is a perfect module, if we want to reach out API frequently, as it supports pretty much everything, like caching,
redirection, proxies, and so on.

+ We will cover the following topics in this chapter:
    + Interacting with Twitter
    + Interacting with Facebook
    + Interacting with reddit

## API introduction
> Before diving into details, let us have a quick look at what exactly is an Application Programming Interface(API).

+ A web API is a set of rules and specifications. It assists us to communicate with different software. There are different types of APIs, and REST API is the subject matter here.
+ REpresentational State Transfer(REST) is an architecture containing guidelines for building scalable web services. An API which adheres to the guidelines and conforms to the constraints of REST is called a RESTful API.
+ In a nutshell, the constraints are:
    + Client-server
    + Stateless
    + Cacheable
    + Layered system
    + Uniform interface
    + Code on demand

+ Google Maps API, Twitter API, and GitHub API are various examples RESTful APIs.

> Take an instance of getting all tweets from Twitter with the hashtag "worldtoday" which includes the process of authenticating, sending requests and receiving responses from different URLs, and dealing with different methods.
> All the said processes and the procedures will be specified in the API of Twitter. By following these procedures, we can collaborate with the web smoothly.


## Getting started with the Twitter API
+ To get started with Twitter API we should first obtain an API key.
    + It is a code which is passed by the computer programs while calling an API.
    + The basic purpose of the API key is that it uniquely identifies the program that it is trying to interact with.
+ It also serves us in the process of authentication with its token.
    + The next step involves the process of creating an authentication request which will give us access to the Twitter account.
+ Once we have authenticated successfully, we will be free to deal with tweets, followers, trends, searches, and stuff.

### Obtaining an API Key
Getting an API key is pretty simple. You need to follow the steps prescribed in the following section:
1. At first, you need to sign into the page https://apps.twitter.com/with your your Twitter credentials.
2. Click on Create New Appbutton.
3. Now, you need to fill the following fields to set up a new application:
    + Name: Specify your application name. This is used to attribute the source of a tweet and in user-facing authorization screens.
    + Description: Enter a short description of your application. This will be shown when a user faces the authorization screens.
    + Website: Specify your fully qualified website URL. A fully qualified URL includes http:// or https:// and will not have a trailing slash in the end (for example: http://example.comor http://www.example.com).
    + Callback URL: This field answers the question—where should we return after successfully authenticating.
    + Developer Agreement: Read the Developer Agreement carefully and then check the checkbox Yes, I agree.
4. Now, by clicking on Create your Twitter application,a new application will be created for us with the previously specified details.
5. After the successful creation, we'll be redirected to a page where the Details tab is selected by default.
    + Now, select the Keys and Access Tokenstab. We should click on Create my access tokenbutton to generate our access token.
6. Lastly, make a note of the Consumer Key (API Key), Consumer Secret (API Secret), Access Token and Access Token Secret.

### Creating an authentication Request
If we remember the theme of the third chapter, we learned different kinds of authentication with requests, such as Basic authentication, Digest authentication, and OAuth authentication. Time to apply all that stuff in real time!
+ Now, we will be using OAuth1 authentication to get the access to the Twitter API.
    + In the first step of obtaining a key, we got access to Consumer key, Consumer secret, Access token and Access token secret, now we should use them to authenticate our application.
+ The following commands show how we can accomplish the process:
```
>>> import requests
>>> from requests_oauthlib import OAuth1
>>> CONSUMER_KEY = 'YOUR_APP_CONSUMER_KEY'
>>> CONSUMER_SECRET = 'YOUR_APP_CONSUMER_SECRET'
>>> ACCESS_TOKEN = 'YOUR_APP_ACCESS_TOKEN'
>>> ACCESS_TOKEN_SECRET = 'YOUR_APP_ACCESS_TOKEN_SECRET'
>>> auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
```

In the preceding lines, we have sent our keys and tokens to the API and got ourselves authenticated and stored them in the variable auth.
> Now, we can do all sorts of interactions with the API using this. Let us start to interact with the Twitter API.

# ----------------------------------------------------------------------------------------- #

# Web Scraping with Python Requests and BeautifulSoup

## Building a web scraping bot – a practical example
At this point of time, our minds got enlightened with all sorts of clues to scrape the Web. With all the information acquired, let's look at a practical example.
Now, we will create a web scraping bot, which will pull a list of words from a web resource and store them in a JSON file.

## The web scraping bot
Here, the web scraping bot is an automated script that has the capability to extract words from a website named majortests.com.
This website consists of various tests and Graduate Record Examinations(GRE) word lists.
With this web scraping bot, we will scrape the previously mentioned website and create a list of GRE words and their meanings in a JSON file.

Before we kickstart the scraping process, let's revise the dos and don't of web scraping as mentioned in the initial part of the chapter.
+ Believe it or not they will definitely leave us in peace:
    + Do refer to the terms and conditions: Yes, before scraping majortests.com, refer to the terms and conditions of the site and obtain the necessary legal permissions to scrape it.
    + Don't bombard the server with a lot of requests: Keeping this in mind, for every request that we are going to send to the website, a delay has been instilled using Python's time.sleepfunction.
    + Do track the web resource from time to time: We ensured that the code runs perfectly with the website that is running on the server. Do check the site once before starting to scrape, so that it won't break the code. This can be made possible by running some unit tests, which conform to the structure we expected.

### Identifying the URL or URLs
The first step in web scraping is to identify the URL or a list of URLs that will result in the required resources.
In this case, our intent is to find all the URLs that result in the expected list of GRE words.

> The following is the list of the URLs of the sites that we are going to scrape:
http://www.majortests.com/gre/wordlist_01,
http://www.majortests.com/gre/wordlist_02,
http://www.majortests.com/gre/wordlist_03,

+ Our aim is to scrape words from nine such URLs, for which we found a common pattern. This will help us to crawl all of them.
+ The common URL pattern for all those URLs is written using Python's string object, as follows: http://www.majortests.com/gre/wordlist_0%d

In our implementation, we define a method called generate_urls, which will generate the required list of URLs using the preceding URL string.

+ The following snippet demonstrates the process in a Python shell:
```
>>> START_PAGE, END_PAGE = 1, 10
>>> URL = "http://www.majortests.com/gre/wordlist_0%d"

>>> def generate_urls(url, start_page, end_page):
        urls = []
        for page in range(start_page, end_page):
            urls.append(url % page)
        return urls

>>> generate_urls(URL, START_PAGE, END_PAGE)
['http://www.majortests.com/gre/wordlist_01', 'http://www.majortests.com/gre/wordlist_02', 'http://www.majortests.com/gre/wordlist_03', 'http://www.majortests.com/gre/wordlist_04', 'http://www.majortests.com/gre/wordlist_05', 'http://www.majortests.com/gre/wordlist_06', 'http://www.majortests.com/gre/wordlist_07', 'http://www.majortests.com/gre/wordlist_08', 'http://www.majortests.com/gre/wordlist_09']
```

### Using an HTTP client
We will use the requests module as an HTTP client to get the web resources:
```
>>> import requests
>>> def get_resource(url):
        return requests.get(url)
>>> get_resource("http://www.majortests.com/gre/wordlist_01")
<Response [200]>
```

+ In the preceding code, the get_resource function takes url as an argument and uses the requests module to get the resource.

### Discovering the pieces of data to scrape
Now, it is time to analyze and classify the contents of the web page. The content in this context is a list of words with their definitions. In order to identify the elements of the words and their definitions, we used Chrome DevTools.
+ The perceived information of the elements (HTML elements) can help us to identify the word and its definition, which can be used in the process of scraping.To carry this out open the URL (http://www.majortests.com/gre/wordlist_01) in the Chrome browser and access the Inspect element option by right-clicking on the web page.

From thepreceding image, we can identify the structure of the word list, which appears in the following manner:
```
<div class="grid_9 alpha">
    <h3>Group 1</h3>
    <a name="1"></a>
    <table class="wordlist">
        <tbody>
            <tr>
                <th>Abhor</th>
                <td>hate</td>
            </tr>
            <tr>
                <th>Bigot</th>
                <td>narrow-minded, prejudiced person</td>
            </tr>
        </tbody>
    </table>
</div>
```

+ By looking at theparts of the previously referred to web page, we can interpret the following:
    + Each web page consists of a word list
    + Every word list has many word groups that are defined in the same divtag
    + All the words in a word group are described in a table having the class attribute—wordlist
    + Each and every table row (tr) in the table represents a word and its definition using the th and td tags, respectively

### Utilizing a web scraping tool
Let's use BeautifulSoup4 as a web scraping tool to parse the obtained web page contents that we received using the requests module in one of the previous steps.
+ By following the preceding interpretations, we can direct BeautifulSoup to access the required content of the web page and deliver it as an object:
```
def make_soup(html_string):
    return BeautifulSoup(html_string)
```

+ In the preceding lines of code, the make_soupmethod takes the htmlcontent in the form of a string and returns a BeautifulSoup object.

### Drawing the desired data
The BeautifulSoup object that we obtained in the previous step is used to extract the required words and their definitions from it.
Now, with the methods available in the BeautifulSoup object, we can navigate through the obtained HTML response, and then we can extract the list of words and their definitions:
```
def get_words_from_soup(soup):
    words = {}
    for count, wordlist_table in enumerate(soup.find_all(class_='wordlist')):
        title = "Group %d" % (count + 1)
        new_words = {}
    for word_entry in wordlist_table.find_all('tr'):
        new_words[word_entry.th.text] = word_entry.td.text
    words[title] = new_words
return words
```

+ In the preceding lines of code, get_words_from_soup takes a BeautifulSoup object and then looks for all the words contained in the wordlists class using the instance's find_all()method, and then returns a dictionary of words.

+ The dictionary of words obtained previously will be saved in a JSON file using the following helper method:
```
def save_as_json(data, output_file):
    """ Writes the given data into the specified output file"""
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile)
```

Entire Example:
```
import json
import time
import requests
from bs4 import BeautifulSoup

START_PAGE, END_PAGE, OUTPUT_FILE = 1, 10, 'words.json'

# Identify the URL
URL = "http://www.majortests.com/gre/wordlist_0%d"

def generate_urls(url, start_page, end_page):
    """This method takes a 'url' and returns a generated list of url strings params: a 'url', 'start_page' number and 'end_page' number. Return value: a list of generated url strings"""
    urls = []
    for page in range(start_page, end_page):
        urls.append(url % page)
    return urls

def get_resource(url):
    """This method takes a 'url' and returns a 'requests.Response' object. Params: a 'url'. Return value: a 'requests.Response' object"""
    return requests.get(url)

def make_soup(html_string):
    """This method takes a 'html string' and returns a 'BeautifulSoup' object params: html page contents as a string return value: a 'BeautifulSoup' object."""
    return BeautifulSoup(html_string)

def get_words_from_soup(soup):
    """This method extracts word groups from a given 'BeautifulSoup' object params: a BeautifulSoup object to extract data return value: a dictionary of extracted word groups"""
    words = {}
    count = 0
    for wordlist_table in soup.find_all(class_='wordlist'):
        count += 1
        title = "Group %d" % count
        new_words = {}
        for word_entry in wordlist_table.find_all('tr'):
            new_words[word_entry.th.text] = word_entry.td.text
        words[title] = new_words
        print " - - Extracted words from %s" % title
    return words

def save_as_json(data, output_file):
    """ Writes the given data into the specified output file"""
    json.dump(data, open(output_file, 'w'))

def scrapper_bot(urls):
    """Scrapper bot: params: takes a list of urls return value: a dictionary of word lists containing different word groups"""
    gre_words = {}
    for url in urls:
        print "Scrapping %s" % url.split('/')[-1]
        # step 1
        # get a 'url'
        # step 2
        html = requets.get(url)
        # step 3
        # identify the desired pieces of data in the url using Browser tools
        #step 4
        soup = make_soup(html.text)
        # step 5
        words = get_words_from_soup(soup)
        gre_words[url.split('/')[-1]] = words
        print "sleeping for 5 seconds now"
        time.sleep(5)
    return gre_words

if __name__ == '__main__':
    urls = generate_urls(URL, START_PAGE, END_PAGE+1)
    gre_words = scrapper_bot(urls)
    save_as_json(gre_words, OUTPUT_FILE)
```

## Summary
+ In this chapter, you learned:
    + about different types of data that we encountered with web sources and tweaked some ideas.
    + We came to know about the need for web scraping, the legal issues, and the goodies that it offers. Then, we jumped deep into web scraping tasks and their potential.
    + You learned about a new library called BeautifulSoup, and its ins and outs, with examples. We came to know the capabilities of BeautifulSoupin depth and  worked on some examples to get a clear idea on it.
    + At last, we created a practical scraping bot by applying the knowledge that we gained from the previous sections, which enlightened us with an experience to scrape a website in real time.

+ In the next chapter, you will learn about the Flask microframework and we will build an application using it by following the best practices.
