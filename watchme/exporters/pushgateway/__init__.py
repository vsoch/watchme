'''

Copyright (C) 2019 Vanessa Sochat
Copyright (C) 2019 Antoine Solnichkin

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from watchme.logger import bot
from watchme.exporters import ExporterBase

class Exporter(ExporterBase):

    required_params = ['url']

    def __init__(self, name, params={}, **kwargs): 

        # Ensure that the user has installed PushGateway
        try:
            from prometheus_client import CollectorRegistry
        except:
            bot.error("prometheus_client module not found.")
            bot.error("pip install watchme[exporter-pushgateway]")
            return

        self.type = 'pushgateway'        
        super(Exporter, self).__init__(name, params, **kwargs)
        self.registry = CollectorRegistry()

    def _validate(self):
        '''this function is called after the ExporterBase validate (checking
           for required params) to ensure that the url param starts with http.
        '''
        if not self.params['url'].startswith('http'):
            bot.exit("url must start with http, found %s" % self.params['url'])

# Push Functions

    def push(self, result, task):
        '''push dummy function, expects the dictionary with commits, dates,
           and results. Since pushgateway only takes numbers, we parse the
           list of content.
        '''
        if "content" in result:
            return self._save_text_list(task.name, result['content'])


# Export Functions

    def export(self, result, task):
        '''the export function is the entrypoint to export data for an
           exporter. Based on the data type, we call any number of supporting
           functions. If True is returned, the data is exported. If False is
           returned, there was an error. If None is returned, there is no
           exporter defined for the data type.
        '''
        # Case 1. The result is a list
        if isinstance(result, list):
                
            # Get rid of Nones, if the user accidentally added
            result = [r for r in result if r]

            if len(result) == 0:
                bot.error('%s returned empty list of results.' % name)

            # Only save if the export type is not json, and the result is a text string
            elif not task.params.get('save_as') == 'json' and not os.path.exists(result[0]):
                bot.info('Exporting list to ' + client.name)
                return self._save_text_list(task.name, result)
                
        # Case 2. The result is a string
        elif isinstance(result, str):
                
            # Only export if it's not a file path (so it's a string)
            if not(os.path.exists(result)):
                bot.info('Exporting text to ' + client.name)
                return self._save_text(result)

        # Case 3. The result is a dictionary or a file, ignore for now.               
        else:
            bot.warning('Files/dictionary are not currently supported for export')

    def _save_text_list(self, name, results):
        '''for a list of general text results, send them to a pushgateway.
           for any error, the calling function should return False immediately.
    
           Parameters
           ==========
           results: list of string results to write to the pushgateway
        '''
        for r in range(len(results)):
            if not self._write_to_pushgateway(results[r]):
                return False
        return True

    def _save_text(self, result):
        '''exports the text to the exporter
 
           Parameters
           ==========
           result: the result object to save, not a path to a file in this case
        '''
        return self._write_to_pushgateway(result)

    def _write_to_pushgateway(self, result):
        ''' writes data to the pushgateway
 
           Parameters
           ==========
           result: the result object to save
        '''
        from prometheus_client import Gauge, push_to_gateway
        
        try:
            g = Gauge(self.name.replace('-', ':'), '', registry=self.registry)
            g.set(result)
            push_to_gateway(self.params['url'], 
                            job='watchme', 
                            registry=self.registry)
        except:
            bot.error('An exception occurred while trying to export data using %s' % self.name)
            return False

        return True
