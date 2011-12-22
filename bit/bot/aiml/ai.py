

import os
from twisted.internet import defer

from bit.bot.aiml.kernel import BitKernel

class BitAI(object):
    def __init__(self,name):
        self.name = name
        self._bot = None

    @property
    def bot(self):
        if self._bot: return self._bot
        self._bot = BitKernel()
        return self._bot

    def learn(self,filepath):
        self.bot.setPredicate('secure', "yes")        
        print 'bot learning: %s' %filepath
        self.bot.learn(filepath)
        self.bot.setPredicate('secure', "no")                                

    def wake(self,verbose=False):  
        print 'waking bot'
        self.bot.verbose(verbose)
        self.bot.setBotPredicate('name', self.name)
        self.bot.setBotPredicate('age', '~180')
        self.bot.setBotPredicate('location', 'Trinity' )
        self.bot.setBotPredicate('gender', 'male' )
        self.bot.setBotPredicate('party', 'libertarian socialist' )        
        return
        self.bot.setPredicate('secure', "yes")        

        aiml_dir = os.path.join(os.path.dirname(__file__),'aiml')
        var_dir = os.path.join(os.getcwd(),'var')                
        
        #self.bot.learn(os.path.join(aiml_dir,'trinity.aiml'))
        #self.bot.setPredicate('secure', "no")                        
        #return
        
        brain = os.path.join(var_dir,"%s.brn" %self.name)
        if os.path.isfile(brain):
            self.bot.bootstrap(brainFile = brain)
        else:
            for ai in os.listdir(aiml_dir):
                if ai.endswith('aiml'):
                    self.bot.learn(os.path.join(aiml_dir,ai))
        #self.bot.saveBrain(brain)
        self.bot.setPredicate('secure', "no")                

    def respond(self,question,session=None):
        return defer.maybeDeferred(self.bot.respond,question,session)
        
