'''

Exporter class : defines properties of an exporter object
Note : No validation is currently done for the exporters.

Author : Antoine Solnichkin
Date : 04/05/2019


'''

class ExporterBase(object):

    required_params = []

    def __init__(self, name, params={}, **kwargs):

        self.name = name
        self.valid = False
        self.params = {}
        self.set_params(params)
        self.validate()

    # Parameters

    def set_params(self, params):
        '''iterate through parameters, set into dictionary.

           Parameters
           ==========
           params: a list of key@value pairs to set.
        '''
        for key,value in params.items():
            key = key.lower()
            self.params[key] = value

    # Validation

    # For now, it should always be valid as no required parameters are defined.
    def validate(self):
        '''validate the parameters set for the Exporter. Exit if there are any
           errors. Ensure required parameters are defined, and have correct
           values.
        '''
        self.valid = True

        for param in self.required_params:
            if param not in self.params:
                bot.error('Missing required parameter: %s' % param)
                self.valid = False