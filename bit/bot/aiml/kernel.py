

import os
import aiml


class BitKernel(aiml.Kernel):
    # <system>
    def _processSystem(self,elem, sessionID):
        """Process a <system> AIML element.

        <system> elements process their contents recursively, and then
        attempt to execute the results as a shell command on the
        server.  The AIML interpreter blocks until the command is
        complete, and then returns the command's output.

        For cross-platform compatibility, any file paths inside
        <system> tags should use Unix-style forward slashes ("/") as a
        directory separator.

        """
        # build up the command string
        command = ""
        for e in elem[2:]:
            command += self._processElement(e, sessionID)

        #HACK
        
        from zope.dottedname.resolve import resolve  

        inputStack = self.getPredicate(self._inputStack, sessionID)
        input = self._subbers['normal'].sub(inputStack[-1])
        # fetch the Kernel's last response (for 'that' context)
        outputHistory = self.getPredicate(self._outputHistory, sessionID)
        try: that = self._subbers['normal'].sub(outputHistory[-1])
        except: that = "" # there might not be any output yet
        topic = self.getPredicate("topic", sessionID)
        if '.' in command and not '/' in command:
            code = resolve(command)
            if code:
                _code = code(self)      
                parser = _code.parse(elem,sessionID,self)
                # use maybedeferred here
                if hasattr(parser,'addCallback'):
                    parser.addCallback(lambda result: _code.complete())
                    return ''
                return parser
        #/HACK


        # normalize the path to the command.  Under Windows, this
        # switches forward-slashes to back-slashes; all system
        # elements should use unix-style paths for cross-platform
        # compatibility.
        #executable,args = command.split(" ", 1)
        #executable = os.path.normpath(executable)
        #command = executable + " " + args
        command = os.path.normpath(command)

        # execute the command.
        response = ""
        try:
            out = os.popen(command)            
        except RuntimeError, msg:
            if self._verboseMode:
                err = "WARNING: RuntimeError while processing \"system\" element:\n%s\n" % msg.encode(self._textEncoding, 'replace')
                sys.stderr.write(err)
            return "There was an error while computing my response.  Please inform my botmaster."
        for line in out:
            response += line + "\n"
        response = string.join(response.splitlines()).strip()
        return response
    
    def respond_async(self, sessionID, response):
        """Return the Kernel's response to the input string."""
        
        # prevent other threads from stomping all over us.
        self._respondLock.acquire()

        self._addSession(sessionID)
        
        # add the data from this exchange to the history lists
        outputHistory = self.getPredicate(self._outputHistory, sessionID)
        outputHistory.append(response)
        while len(outputHistory) > self._maxHistorySize:
            outputHistory.pop(0)
            self.setPredicate(self._outputHistory, outputHistory, sessionID)
         
        # release the lock and return
        self._respondLock.release()
