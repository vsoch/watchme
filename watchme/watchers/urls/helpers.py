'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

import os
import tempfile
import requests
import re

# Helper functions

def get_params(kwargs, key='url_param_'):
    '''a general function to get parameter sets based on a user input. 
       Returns a list of dictionaries, one per set.

       Parameters
       ==========
       kwargs: the dictionary of keyword arguments that may contain url
               parameters (format is url_param_<name>
       key: the string that the parameters start with (defaults to url_param)
    '''
    # Keey dictionary based on index of param
    params = {}

    names = [x for x in kwargs if x.startswith(key)]
    for n in range(len(names)):
        name = names[n]

        # Params are split by commas, with index corresponding to list index
        paramlist = kwargs.get(name).split(',')

        # Remove the "url_param"
        name = name.replace(key, '', 1)

        # Update the dictionary of dictionaries
        for i in range(len(paramlist)):

            # Add the index to the dicionary (will be turned in list later)
            if i not in params:
                params[i] = {}

            if paramlist[i] != '':
                params[i][name] = paramlist[i]

    # Unwrap the list
    params = [x for x in params.values()]

    # If no special params, we at least need to run once
    if len(params) == 0:
        params = [{}]

    return params


def parse_success_response(response, kwargs):
    '''parse a successful response of 200, meaning we honor the user
       request to return json, search for a regular expression, or return
       raw text. This is used by the basic GET/POST functions. For parsing
       with beautiful soup, see "get_results" and "get_url_selection"

       Parameters
       ==========
       response: the requests (200) response
       kwargs: dictionary of keyword arguments provided to function
    '''
    result = None
    save_as = kwargs.get('save_as', 'json')
    regex = kwargs.get('regex')

    # Returning the result as json will detect dictionary, and save json
    if save_as == "json":
        result = response.json()

    # As an alternative, search for a regular expression
    elif regex not in ["", None]:
        match = re.search(regex, response.text)
        result = match.group()

    # Otherwise, we return text
    else:
        result = response.text
    return result


def get_headers(kwargs):
    '''Get a single set of headers from the kwargs dict. A user agent is added
       as it is helpful in most cases.

       Parameters
       ==========
       kwargs: the dictionary of keyword arguments that may contain url
               parameters (format is url_param_<name>
    '''
    headers = {"User-Agent": "Mozilla/5.0"}

    for key, value in kwargs.items():
        if key.startswith('header_'):
            name = key.replace('header_', '', 1)

            # The header is defined with a value
            if value != None:
                headers[name] = value

            # If the user wants to remove the User-Agent (or any) header
            elif value == None and name in headers:
                del headers[name]

    return headers


def get_results(url, 
                selector,
                func=None,
                attributes=None,
                params={},
                get_text=False,
                headers={},
                regex=None):

    '''given a url, a function, an optional selector, optional attributes, 
       and a set (dict) of parameters, perform a request. This function is
       used if the calling function needs special parsing of the html with
       beautiful soup. If only a post/get is needed, this is not necessary.

       Parameters
       ==========
       url: the url to get (required)
       func: the function to use, defaults to requests.get
       selector:  selection for the html response
       attributes: optional, a list of attributes
       params: a dictionary of parameters
       headers: a dictionary of header key value pairs
    '''
    from bs4 import BeautifulSoup

    if func == None:
        func = requests.get

    response = func(url, params=params, headers=headers)
    results = []

    if response.status_code == 200:   
        soup = BeautifulSoup(response.text, 'lxml')

        # Get the selection
        for entry in soup.select(selector):

            # Does the user want to get attributes
            if attributes != None:
                [results.append(entry.get(x)) for x in attributes]

            # Second priority for regular expression on text
            elif regex not in [None, ""]:
                match = re.search(regex, entry.text)
                results.append(match.group())

            # Does the user want to get text?
            elif get_text == True:
                results.append(entry.text)

            # Otherwise, return the entire thing
            else:
                results.append(str(entry))

    # Clean up results
    results = [x for x in results if x]

    return results
