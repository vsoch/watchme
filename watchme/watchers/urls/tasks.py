'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.utils import generate_temporary_file
from watchme.logger import bot
from .helpers import (
    get_params, 
    get_results, 
    get_headers,
    parse_success_response
)
from requests.exceptions import HTTPError
import os
import re
import tempfile
import requests


def get_task(url, **kwargs):
    '''a simple task to use requests to get a url. By default, we return
       the raw response.

       Parameters
       ==========

       REQUIRED:
           url: a url to return the page for

       OPTIONAL
           regex: a regular expression to search the text for (not used w/ json)
           save_as: return the result to save as json
    '''
    results = []
    paramsets = get_params(kwargs)
    headers = get_headers(kwargs)

    for params in paramsets:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:

            # Parse the response per the user's request
            result = parse_success_response(response, kwargs)
            results.append(result)

    results = [x for x in results if x]
 
    if len(results) == 0:
        results = None

    return results


def post_task(url, **kwargs):
    '''a simple task to use requests to post to. By default, we return json.

       Parameters
       ==========

       REQUIRED:
           url: a url to post to
    '''
    results = []

    # The json params can vary, but headers do not
    jsonlist = get_params(kwargs, key='json_param_')
    headers = get_headers(kwargs)

    # Loop through lists of json and headers
    for params in jsonlist:

        # Get the post response and proceed if successful
        response = requests.post(url, json=params, headers=headers)
        if response.status_code == 200:

            # Parse the response per the user's request
            result = parse_success_response(response, kwargs)
            results.append(result)

        else:
            bot.error("%s: %s" %(response.status_code, response.reason))

    results = [x for x in results if x]

    # Return None if no results found
    if len(results) == 0:
        results = None

    return results


def download_task(url, **kwargs):
    '''a simple task to use requests to get a url. By default, we return
       the raw response.

       Parameters
       ==========

       REQUIRED:
           url: a url to download (stream)

       OPTIONAL:
           write_format: to change from default "w"
           disable_ssl_check: set to anything to not verify (not recommended)
    '''
    result = None

    # Update the user what we are doing
    bot.verbose("Downloading %s" % url)

    # Use the basename or the user set file_name to write to
    file_name = kwargs.get('file_name', os.path.basename(url))
    destination = os.path.join(tempfile.gettempdir(), file_name)    
    verify = True

    # Does the user want to disable ssl?
    if "disable_ssl_check" in kwargs:
        if kwargs['disable_ssl_check']:
            bot.warning('Verify of certificates disabled! ::TESTING USE ONLY::')
            verify = False

    # If the user doesn't want to write, but maybe write binary
    fmt = kwargs.get('write_format', 'wb')
    headers = get_headers(kwargs)

    # Does the url being requested exist?
    if requests.head(url, verify=verify, headers=headers).status_code in [200, 401]:

        # Stream the response
        response = requests.get(url, verify=verify, stream=True, headers=headers)

        # Invalid permissions
        if response.status_code == 401:
            return result

        # Successful, stream to result destination
        if response.status_code == 200:

            chunk_size = 1 << 20
            with open(destination, fmt) as filey:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    filey.write(chunk)

            result = destination

    return result


def get_url_selection(url, **kwargs):
    '''select some content from a page dynamically, using selenium.

       Parameters
       ==========
       kwargs: a dictionary of key, value pairs provided by the user
    '''
    
    results = None
    selector = kwargs.get('selection', None)
    headers = get_headers(kwargs)

    if selector == None:
        bot.error('You must define the selection (e.g., selection@.main')
        return results

    # Does the user want to get text?
    get_text = False
    if kwargs.get('get_text') != None:
        get_text = True

    # Are we searching for a regular expression in the result?
    regex = kwargs.get('regex')

    # Does the user want to get one or more attributes?
    attributes = kwargs.get('attributes', None)
    if attributes != None:
        attributes = attributes.split(',') 

    # User can pass a parameter like url_param_<name>
    # url_param_page=1,2,3,4,5,6,7,8,9
    paramsets = get_params(kwargs)

    # Each is a dictionary of values
    results = []
    for params in paramsets:
 
        # Get the page
        results += get_results(url=url,
                               selector=selector,
                               headers=headers,
                               attributes=attributes,
                               params=params,
                               get_text=get_text,
                               regex=regex)

    # No results
    if len(results) == 0:
        results = None

    return results
