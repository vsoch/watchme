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
        self.registry = CollectorRegistry()
        
        super(Exporter, self).__init__(name, params, **kwargs)

    def _save_text_list(self, name, results):
        '''for a list of general text results, send them to a pushgateway.
 
           Parameters
           ==========
           results: list of string results to write to the pushgateway
        '''
        for r in range(len(results)):
            self._write_to_pushgateway(results[r])


    def _save_text(self, result):
        '''exports the text to the exporter
 
           Parameters
           ==========
           result: the result object to save, not a path to a file in this case
        '''
        self._write_to_pushgateway(result)


    def _write_to_pushgateway(self, result):
        ''' writes data to the pushgateway
 
           Parameters
           ==========
           result: the result object to save
        '''
        from prometheus_client import Gauge, push_to_gateway
        g = Gauge(self.name.replace('-', ':'), '', registry=self.registry)
        g.set(result)
        
        try:
            push_to_gateway(self.params['url'], 
                            job='watchme', 
                            registry=self.registry)
        except:
            bot.error('An exception occurred while trying to export data using %s' % self.name)

            #TODO: disable task, and add a --test command
            #TODO: need commands to add/remove exporters from a task
