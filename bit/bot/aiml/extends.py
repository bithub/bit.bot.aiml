
import os, inspect
from zope.interface import implements
from zope.component import getUtility,provideUtility,provideAdapter

from bit.core.interfaces import IPlugin, IConfiguration, IPluginExtender
from bit.bot.common.interfaces import  IIntelligent

class AIMLPlugin(object):
   implements(IPluginExtender)
   def __init__(self,plugin):
       self.plugin = plugin

   def extend(self):
       if hasattr(self.plugin,'load_AIML'):
           getattr(self.plugin,'load_AIML')()      
       else:
           fpath =  os.path.dirname(inspect.getfile(self.plugin.__class__))
           aiml_paths = getattr(self.plugin,'_aiml',[])
           for aiml in aiml_paths:
               target = os.path.join(fpath,aiml)
               if os.path.isdir(target):
                   for f in os.listdir(target):
                       if f.endswith('.aiml'):
                           getUtility(IIntelligent).learn(os.path.join(target,f))
               elif os.path.isfile(target):
                   getUtility(IIntelligent).learn(target)
