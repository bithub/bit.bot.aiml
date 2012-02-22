
import zope
import os
import bit

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('bit.core')

class IAIMLDirective(zope.interface.Interface):
    """
    Define a aiml
    """
    filepath = zope.configuration.fields.Path(
        title=_("File path"),
        description=_("The directory system file path"),       
        required=True,
        )

def aiml(_context, filepath):
    if os.path.isdir(filepath):
        for f in os.listdir(filepath):
            if f.endswith('.aiml') and os.path.isfile(os.path.join(filepath,f)):
                _context.action(
                    discriminator = None,
                    callable = zope.component.getUtility(bit.bot.common.interfaces.IIntelligent).learn,
                    args = (os.path.join(filepath,f),)
                    )
    elif os.path.isfile(filepath):
        _context.action(
            discriminator = None,
            callable = zope.component.getUtility(bit.bot.common.interfaces.IIntelligent).learn,
            args = (filepath,)
            )


        

