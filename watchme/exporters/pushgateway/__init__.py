'''

Copyright (C) 2019 Antoine Solnichkin.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


'''

from watchme.exporters import ExporterBase

class Exporter(ExporterBase):

    required_params = ['url']

    def __init__(self, name, params={}, **kwargs): 

        self.type = 'pushgateway'

        super(Exporter, self).__init__(name, params, **kwargs)