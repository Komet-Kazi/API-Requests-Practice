# Accessing the different endpoints offered by the open-notify api

import requests
import json
import http
import logging
import datetime

logging.basicConfig(filename=f'{__file__}.log', level=logging.DEBUG, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# Changing the logging debug level greater than 0 will log the response HTTP headers to stdout.
# useful if you're dealing with an API that returns a large body payload that is not suitable for logging or contains binary content.
http.client.HTTPConnection.debuglevel = 1

# International Space Station Location
# Documentation: http://open-notify.org/Open-Notify-API/ISS-Location-Now/
# EndPoint: http://api.open-notify.org/iss-now.json
def get_ISS_Position():
    '''
    Params: None
    Returns: latitude and longitude of the space station and a unix timestamp for the time the location was valid.
    '''

    response = requests.get(r'http://api.open-notify.org/iss-now.json')  # Get request with no additional params

    logging.debug(f'Status: {response.status_code}')
    logging.debug(f'Response: {jPrint(response.json())}')

    epochTime = response.json()['timestamp']
    timeStamp = datetime.datetime.fromtimestamp(epochTime)

    issLatitude = response.json()['iss_position']['latitude']
    issLongitude = response.json()['iss_position']['longitude']

    logging.info(f'\nTime: {str(timeStamp)}\n\tLatitude: {issLatitude}\n\tLongitude: {issLongitude}')

# International Space Station pass times
# Documentation: http://open-notify.org/Open-Notify-API/ISS-Pass-Times/
# EndPoint: http://api.open-notify.org/iss-pass.json
# Query strings:
# lat = latitude > Accepted values range(-80,80)
# lon = longitude > Accepted values range(-180,180)
# alt = altitude > Accepted values range(0,10000)
# n = number of passes > Accepted values range(1,100)
def when_ISS_Overhead(latitude, longitude, altitude=1, number=1):
    '''
    This function will make an API call requesting a list of times the ISS will be overhead.
    Required Parameters:
        latitude - latitude(degrees) of the place to predict passes
        longitude - longitude(degrees) of the place to predict passes
    Optional Parameters:
        altitude - The altitude(meters) of the place to predict passes defaults to 1
        number - The number of passes to return defaults to 1
    '''
    parameters = {
        'lat': latitude,
        'lon': longitude,
        'alt': altitude,
        'n': number
    }

    response = requests.get(r'http://api.open-notify.org/iss-pass.json', params=parameters)  # Get request with additional params

    logging.debug(f'Status: {response.status_code}')
    logging.debug(f'Response: {jPrint(response.json())}')

    pass_times = response.json()['response']  # extract the part of the response needed


    # pass_times is a list of dictionaries
    # each dictionary has a 'duration' key and a 'risetime' key
    for pt in pass_times:
        epochTime = pt['risetime']

        # we need to convert the epoch timestamps to something readable
        time = datetime.datetime.fromtimestamp(epochTime)
        logging.debug(f'Time: {time}')
        print(f'The ISS will pass overhead on {time.date()} at {time.time()}')
        logging.info(f'The ISS will pass overhead on {time.date()} at {time.time()}')

# People in Space
# Documentation: http://open-notify.org/Open-Notify-API/People-In-Space/
# EndPoint: http://api.open-notify.org/astros.json
def get_Astronauts():
    '''
    This API takes no inputs.
    Returns: Number of people in space. When known it also returns the names and spacecraft those people are on.
    '''
    response = requests.get(r'http://api.open-notify.org/astros.json')  # Get request with no additional params
    logging.debug(f'Status: {response.status_code}')
    logging.debug(f'{jPrint(response.json())}')  # View entire response

    # Extract number of astronauts
    astro_count = response.json()['number']
    print(f'Number of astronauts in space: {astro_count}')

    # Extract list of dictionaries 'people'
    # Each dictionary has a 'name' key and 'craft' key
    people = response.json()['people']

    for person in people:
        name = person['name']
        craft = person['craft']

        logging.info(f'{name} is currently in space aboard the {craft}')
        print((f'{name} is currently in space aboard the {craft}'))


def jPrint(obj):
    '''Format a json object into a formatted string
    Returns: formated string
    '''
    return json.dumps(obj, sort_keys=True, indent=4)

if __name__ == "__main__":
    logging.info('------------ISS Postion------------')
    get_ISS_Position()  # Successful!
    logging.info('------------ISS Overhead------------')
    when_ISS_Overhead(32.2123, -110.879, number=4)  # Successful!
    logging.info('------------Astronauts in space------------')
    get_Astronauts()  # Successful
