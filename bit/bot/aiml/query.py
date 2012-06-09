import time
import datetime

from zope.interface import implements
from zope.component import getAdapters, getUtility

from twisted.internet import defer


from bit.bot.aiml.interfaces\
    import IWhere, IWhereProvider,\
    IWhat, IWhatProvider,\
    IWho, IWhoProvider

from bit.bot.common.interfaces import IIntelligent

from bit.bot.aiml.numeric import NumericStringParser


class WhoProvider(object):
    implements(IWhoProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def search(self, query):
        ai = getUtility(IIntelligent)

        if query.lower() in ['i', 'me']:
            return 'you are %s' % ai.bot.getPredicate('name', self.request.session_id)

        if query.lower() in ['you']:
            return 'i am %s' % ai.name


class WhereProvider(object):
    implements(IWhereProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def search(self, query):
        if query.lower() in ['i', 'me']:
            return 'you are there, in front of the screen'

        if query.lower() in ['you']:
            return 'i am here'


class Who(object):
    implements(IWho)

    def search(self, request, query, providers=None):
        adapters = getAdapters([self, request], IWhoProvider)
        for name, adapter in adapters:
            result =  adapter.search(query)
            if result:
                return result


class Where(object):
    implements(IWhere)

    def search(self, request, query, providers=None):
        adapters = getAdapters([self, request], IWhereProvider)
        for name, adapter in adapters:
            result =  adapter.search(query)
            if result:
                return result


class What(object):
    implements(IWhat)

    def search(self, request, query, providers=None):
        adapters = getAdapters([self, request], IWhatProvider)
        d = None
        for name, adapter in adapters:
            _d = defer.maybeDeferred(adapter.search, query)
            if not d:
                d = _d
            else:
                
                def _result(res, _d):
                    if res:
                        return res
                    else:
                        return _d
                d.addCallback(_result, _d)
        no_results = 'I dont know what %s is' %query                
        def _results(res):            
            if not res:
                return no_results 
            return res
        if not d:
            return no_results

        return d.addCallbacks(_results)


class WhatArithmeticProvider(object):
    implements(IWhatProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def search(self, query, providers=None):
        nmp = NumericStringParser()
        try:
            return str(nmp.eval(query))
        except:
            return


class WhatCharacterProvider(object):
    implements(IWhatProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def search(self, query, providers=None):
        try:
            num = int(query)
            if str(num) == query:
                return '%s is a number' % query
        except:
            pass

        try:
            num = float(query)
            if str(num) == query:
                return '%s is a floating point number' % query
        except:
            pass

        
        if len(query.strip()) != 1:
            return
        
        if query.lower() in map(chr, range(97, 123)):
            return '%s is a letter' %query


class WhatTemporalProvider(object):
    implements(IWhatProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def search(self, query, providers=None):
        tokens = query.split()

        if tokens[0] == 'the':
            del tokens[0]

        if tokens[0] == 'unixtime':
            return str(time.time())

        if tokens[0] == 'time':
            return time.strftime('%H:%m %Z')

        if tokens[0] == 'day':
            return datetime.datetime.now().strftime('%A')

        if tokens[0] == 'date':
            return datetime.datetime.now().strftime('%d/%m/%Y')


class WhatInfoProvider(object):
    implements(IWhatProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def search(self, query, providers=None):
        tokens = query.split()

        if tokens[0] not in ['my', 'your']:
            return

        ai = getUtility(IIntelligent)

        whose = tokens[0]
        del tokens[0]

        if whose == 'my':
            if tokens[0] == 'name':                
                return 'you are %s' % ai.bot.getPredicate('name', self.request.session_id)

            if tokens[0] == 'session':
                return self.request.session_id

        else:
            if tokens[0] == 'name':
                return 'i am %s' % ai.name
