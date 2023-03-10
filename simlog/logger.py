
class HLogger:
    def __init__(self, base_context):
        self._context = base_context
        self._subloggers = {}

    # def store_result(self, keys: SimulationParams, value):
    #     pass

    def create_sublogger(self, context):
        sublogger = HLogger(self._context + context)
        #self._subloggers.append( sublogger )
        self._subloggers[ tuple(context) ] = sublogger
        return sublogger

