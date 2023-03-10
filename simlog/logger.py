import os

import numpy

def ensurePathExists(fn):
    "Assumes that fn consists of a basepath (folder) and a filename, and ensures that the folder exists."
    path = os.path.split(fn)[0]

    if not os.path.exists(path):
        #oldMask = os.umask(0002)
        os.makedirs(path)

class HLogger:
    HIGH = 30
    MEDIUM = 20
    LOW = 10
    def __init__(self, base_context):
        self._base_context = base_context
        self._context = base_context
        self._output_level = self.MEDIUM

    def set_output_level(self, level):
        self._output_level = level

    def set_prefix_context(self, context):
        self._context = self._base_context + context

    def log_append(self, content, relative_context : list, level : int = MEDIUM):
        if level < self._output_level:
            return
        fn = self._get_fn(relative_context)
        outF = open(fn, 'a')
        outF.write(str(content) + ',')
        outF.close()

    def log_histogram(self, content, relative_context : list, level : int = MEDIUM):
        if level < self._output_level:
            return
        #ignoring histogram for now..
        self.log_raw_numbers([x for x in content], relative_context, level)

    def log_raw_numbers(self, content, relative_context : list, level : int = MEDIUM):
        if level < self._output_level:
            return
        fn = self._get_fn(relative_context)
        assert isinstance(content,list), type(content) #just for now..
        outF = open(fn, 'w')
        for el in content:
            if isinstance(el, numpy.ndarray): #just for now
                outF.write(','.join([str(x) for x in el]) + '\n')
            else:
                outF.write(str(el) + ',')
        outF.close()

    def _get_fn(self, relative_context):
        context = self._context + relative_context
        fn = '/'.join(context) + '.csv'
        ensurePathExists(fn)
        return fn
