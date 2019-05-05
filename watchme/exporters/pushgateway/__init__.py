'''

Copyright (C) 2019 Antoine Solnichkin.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


'''

from watchme.exporters import ExporterBase

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class Exporter(ExporterBase):

    required_params = ['url']

    def __init__(self, name, params={}, **kwargs): 

        self.type = 'pushgateway'

        super(Exporter, self).__init__(name, params, **kwargs)

    def _save_text_list(self, name, results):
        '''for a list of general text results, send them to a pushgateway.
 
           Parameters
           ==========
           results: list of string results to write to the pushgateway
        '''
        registry = CollectorRegistry()
        for r in range(len(results)):
            result = results[r]
            g = Gauge(name.replace('-', ':'), '', registry=registry)
            g.set(result)
            push_to_gateway(self.params['url'], job='watchme', registry=registry)