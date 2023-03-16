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
    def __init__(self, base_context, output_level = MEDIUM):
        self._base_context = base_context
        self._extra_contexts = []
        self._output_level = output_level

    def _get_context(self):
        list_of_strings = self._base_context + [item for sublist in self._extra_contexts for item in sublist]
        return list_of_strings

    def log_append(self, content, relative_context : list = [], level : int = MEDIUM):
        if level < self._output_level:
            return
        fn = self._get_fn(relative_context)
        with open(fn, 'a') as outF:
            outF.write(str(content) + ',')

    def log_histogram(self, content, relative_context : list = [], level : int = MEDIUM):
        if level < self._output_level:
            return
        #ignoring histogram for now..
        self.log_raw_numbers([x for x in content], relative_context, level)

    def log_raw_numbers(self, content, relative_context : list = [], level : int = MEDIUM):
        assert isinstance(content,list), type(content) #just for now..
        if level < self._output_level:
            return
        fn = self._get_fn(relative_context)
        with open(fn, 'w') as outF:
            for el in content:
                if isinstance(el, numpy.ndarray): #just for now, this function should of course be much more general
                    outF.write(','.join([str(x) for x in el]) + '\n')
                else:
                    outF.write(str(el) + ',')

    def log_raw_text(self, content, relative_context : list = [], level : int = MEDIUM):
        assert isinstance(content,str), type(content)
        if level < self._output_level:
            return
        fn = self._get_fn(relative_context)
        with open(fn, 'w') as outF:
            outF.write(content)
        

    def log_dict(self, content : dict, relative_context : list = [], level : int = MEDIUM):
        assert isinstance(content, dict)
        if level < self._output_level:
            return
        fn = self._get_fn(relative_context)
        with open(fn, 'w') as outF:
            outF.write('\n'.join([':'.join([str(key),str(val)]) for key,val in content.items()]))

    def _get_fn(self, relative_context):
        context = self._get_context() + relative_context
        fn = '/'.join(context) + '.csv'
        ensurePathExists(fn)
        return fn

    def innerContext(self, context):
        return InnerContext(self, context)

class InnerContext:
    def __init__(self, logger : HLogger, context : list):
        self._logger = logger
        self._context = context

    def __enter__(self):
        self._logger._extra_contexts.append(self._context)

    def __exit__(self, *args):
        self._logger._extra_contexts.pop()

    def iter(self, iterable):
        short_context = self._context[:-1]
        prefix = self._context[-1]
        
        loop_context = InnerContext(self._logger, short_context + [f"{prefix}"])
        for i, item in enumerate(iterable):
            loop_context._context[-1] = f"{prefix}{i}"
            with loop_context:
                yield item

    def range(self, *args):
        short_context = self._context[:-1]
        prefix = self._context[-1]
        
        loop_context = InnerContext(self._logger, short_context + [f"{prefix}"])
        for i in range(*args):
            loop_context._context[-1] = f"{prefix}{i}"
            with loop_context:
                yield i

    def enumerate(self, *args):
        short_context = self._context[:-1]
        prefix = self._context[-1]

        loop_context = InnerContext(self._logger, short_context + [f"{prefix}"])
        for i, item in enumerate(*args):
            loop_context._context[-1] = f"{prefix}{i}"
            with loop_context:
                yield i, item