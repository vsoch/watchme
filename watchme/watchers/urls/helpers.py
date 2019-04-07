'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

import os
import tempfile
import requests

# Helper functions

def get_params(kwargs):
    '''a general function to get parameter sets based on a user input. 
       Returns a list of dictionaries, one per set.

       Parameters
       ==========
       kwargs: the dictionary of keyword arguments that may contain url
               parameters (format is url_param_<name>
    '''
    # Keey dictionary based on index of param
    params = {}

    names = [x for x in kwargs if x.startswith('url_param')]
    for n in range(len(names)):
        name = names[n]
        # Params are split by commas, with index corresponding to list index
        paramlist = kwargs.get(name).split(',')
        # Remove the "url_param"
        name = name.replace('url_param_', '', 1)
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


def get_results(url, selector, func=None, attributes=None, params={}, get_text=False):
    '''given a url, a function, an optional selector, optional attributes, and a set (dict)
       of parameters, perform a request.

       Parameters
       ==========
       url: the url to get (required)
       func: the function to use, defaults to requests.get
       selector:  selection for the html response
       attributes: optional, a list of attributes
       params: a dictionary of parameters
    '''
    from bs4 import BeautifulSoup

    if func == None:
        func = requests.get

    response = func(url, params=params)
    results = []

    if response.status_code == 200:   
        soup = BeautifulSoup(response.text, 'lxml')

        # Get the selection
        for entry in soup.select(selector):

            # Does the user want to get attributes
            if attributes != None:
                [results.append(entry.get(x)) for x in attributes]

            # Does the user want to get text?
            elif get_text == True:
                results.append(entry.text)

            # Otherwise, return the entire thing
            else:
                results.append(str(entry))

    # Clean up results
    results = [x for x in results if x]

    return results
