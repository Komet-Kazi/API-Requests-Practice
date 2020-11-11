# Application name: LastAppi
# API key: 1076a2a4620f9419699125e7244304ef
# Documentation: https://www.last.fm/api
# BaseURL: http://ws.audioscrobbler.com/2.0/
# Example: http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key=YOUR_API_KEY&format=json

# Api key must be provided
# Please use an identifiable User-Agent header on all requests.
# Use UTF-8 encoding when sending arguments to API methods.

# We don’t need to authenticate as a specific Last.fm user.
# All write services require authentication.

# It looks like there is only one real endpoint, and each “endpoint” is actually specified by using the method parameter.

# page (Optional) : The page number to fetch. Defaults to first page.
# limit (Optional) : The number of results to fetch per page. Defaults to 50.
# api_key (Required) : A Last.fm API key.
# EndPoint: chart.getTopArtists


import requests
import requests_cache
import json
import http
import logging
import datetime
import time
import pandas as pd
from tqdm import tqdm

logging.basicConfig(filename=f'{__file__}.log', level=logging.DEBUG, filemode='w', format='%(levelname)s:\n%(message)s\n')

# Changing the logging debug level greater than 0 will log the response HTTP headers to stdout.
# useful if you're dealing with an API that returns a large body payload that is not suitable for logging or contains binary content.
http.client.HTTPConnection.debuglevel = 1

requests_cache.install_cache()

API_KEY = '**********************************'
USER_AGENT = 'LastAppi'

def get_TopArtists():
    '''get the top artists utilizing Last.FM API'''

    payload = {'method': 'chart.gettopartists'}

    response = lastfm_get(payload)

    #logging.debug(f'Response:\n{jprint(response.json())}')
    # response contains dictionary with 'artists' key, containing:
    #### '@attr' key = various response attributes
    #### 'artist' key = list of artist objects

    logging.debug(f'@attr:\n{jprint(response.json()["artists"]["@attr"])}')
    # @attr:{
    # "page": "1",
    # "perPage": "50",
    # "total": "3723977",
    # "totalPages": "74480"}

    total_pages = response.json()["artists"]["@attr"]["totalPages"]
    print(total_pages)


def get_Paginated():
    '''gets paginated results from last.fm API
    returns:
    '''

    # initialize list to hold results
    result_pages = []

    # set initial page and high total number
    current_page = 1
    total_pages = 5 # just a dummy number to start loop

    # iterate over page number to get more result pages
    while current_page <= total_pages:
        logging.debug(f'Requesting page {current_page}/{total_pages}')

        # construct dictionary for payload
        payload = {
            'method': 'chart.gettopartists',
            'limit': 500,
            'page': current_page
            }

        # make the API Call
        response = lastfm_get(payload)

        # if we get an error, print the response and halt the loop
        if response.status_code != 200:
            logging.error(response.text)
            break

        # Extract pagination details and update current_page and total_pages
        current_page = int(response.json()["artists"]["@attr"]["page"])
        #total_pages = int(response.json()["artists"]["@attr"]["totalPages"])


        # Add response to list
        result_pages.append(response)

        # If not from cached sleep for .25 second
        if not getattr(response, 'from_cached', False):
            time.sleep(0.25)

        # Next page
        current_page += 1

    print(len(result_pages))
    return result_pages

    # Using a local database to cache the results of any API call
    #### You don’t make extra API calls that you don’t need to.
    #### You don’t need to wait the extra time to rate limit when reading the repeated calls from the cache.

def process_responses(responses):
    # Look at first responses data
    #r0 = responses[0]
    #r0_json = r0.json()
    #r0_artists = r0_json['artists']['artist']
    #r0_df = pd.DataFrame(r0_artists)
    #r0_df.head()

    # using list comprehension turn each response into a dataframe
    frames = [pd.DataFrame(r.json()['artists']['artist']) for r in responses]

    # combine all the Dataframes into one
    artists = pd.concat(frames)
    #artists.head()

    # Remove the image column
    artists = artists.drop('image', axis=1)

    # Remove Duplicates
    artists = artists.drop_duplicates().reset_index(drop=True)

    tqdm.pandas()
    # get_ArtistTags for each artist name in our artists dataframe
    # displays a progress bar
    artists['tags'] = artists['name'].progress_apply(get_ArtistTags)

    logging.info(f'{artists.head()}')
    logging.info(f'{artists.describe()}')

    return artists

def convertAndExport(artists):
    # convert the listeners and playcount columns to numeric values
    artists[["playcount", "listeners"]] = artists[["playcount", "listeners"]].astype(int)

    # sort by listeners
    artists = artists.sort_values("listeners", ascending=False)

    logging.info(f'{artists.head(10)}')

    artists.to_csv('artists.csv', index=False)
    logging.info('File Saved')

def get_ArtistTags(artist_name):
    payload = {
        'method': 'artist.getTopTags',
        'artist': artist_name
    }

    response = lastfm_get(payload)

    # if there's an error, just return nothing
    if response.status_code != 200:
        logging.error('Error getting tags')
        return None

    # rate limiting
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)

    # extract the top three tags and turn them into a string
    try:
        tags = [tag['name'] for tag in response.json()['toptags']['tag'][:3]]
        tags_str = ', '.join(tags)
        return tags_str
    except KeyError as err:
        logging.debug(err)
        return None


def lastfm_get(payload):
    '''A function that sends a request to the Last.FM API.
    Adds the User agent to headers
    adds api key, and format key to payload
    sends request to url
    params: payload = a dictionary with k,v = 'method', 'chart.get_topartists'
    Returns: Response object
    '''

    # Define headers and URL
    myHeaders = {'user-agent': USER_AGENT}
    URL = r'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(URL, headers=myHeaders, params=payload, timeout=3.5)
    logging.debug(f'Status: {response.status_code}')

    # if there's an error, just return nothing
    if response.status_code != 200:
        logging.error('Error getting tags')
        return None
    return response

def jprint(obj):
    '''Format a json object into a formatted string
    Returns: formated string
    '''
    return json.dumps(obj, sort_keys=True, indent=2)

if __name__ == "__main__":
    #get_TopArtists()  # Successful
    responses = get_Paginated()  # Successful
    df = process_responses(responses)  # Successful
    convertAndExport(df)  # Successful
