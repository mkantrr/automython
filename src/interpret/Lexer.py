import re

import interpret.Buffer as buffer
import interpret.Token as token

EOF = 'EOF'
EOL = 'EOL'
STRING = 'STRING'
VAR = 'VARIABLE'
LITERAL = 'LITERAL'
INTEGER = 'INTEGER'
BOOLEAN = 'BOOLEAN'
PRINT = 'PRINT'
DFA = 'DFA'
NFA = 'NFA'
FUNCTION_CALL = 'FUNCTION_CALL'

class TokenError(ValueError):
    """ The expected token cannot be found """
    def __init__(self, msg=""):
        self.msg = msg
        super().__init__(self.msg)
    
class Lexer:
    def __init__(self, text=''):
        self._text_storage = buffer.Buffer(text)
        self._status = []
        self._current_token = None
        
    def __enter__(self):
        self.stash()

    def __exit__(self, etype, evalue, etrace):
        if etype:
            self.pop()

        if etype in [TokenError]:
            return True

    def load(self, text):
        self._text_storage.load(text)

    def get_token(self):
        eof = self._process_eof()
        if eof:
            return eof

        eol = self._process_eol()
        if eol:
            return eol
          
        self._process_whitespace()
        
        print = self._process_print()
        if print:
            return print
        
        dfa = self._process_dfa()
        if dfa:
            return dfa
        
        nfa = self._process_nfa()
        if nfa:
            return nfa
        
        func_name = self._process_func_name()
        if func_name:
            return func_name

        boolean = self._process_boolean()
        if boolean:
            return boolean
        
        var = self._process_var()
        if var:
            return var
        
        string = self._process_string()
        if string:
            return string
        
        number = self._process_number()
        if number:
            return number
        
        literal = self._process_literal()
        if literal:
            return literal

    def get_tokens(self):
        t = self.get_token()
        tokens = []

        while t != token.Token('EOF'):
            tokens.append(t)
            t = self.get_token()

        tokens.append(token.Token('EOF'))

        return tokens
    
    @property
    def _current_status(self):
        status = {}
        status['text_storage'] = self._text_storage.position
        status['current_token'] = self._current_token
        return status

    def stash(self):
        self._status.append(self._current_status)

    def pop(self):
        status = self._status.pop()
        self._text_storage.goto(*status['text_storage'])
        self._current_token = status['current_token']
    
    def peek_token(self, amount=1):
        self.stash()
        for i in range(amount):
            token = self.get_token()
        self.pop()

        return token
     
    @property
    def line(self):
        return self._text_storage.line 
    
    @property
    def column(self):
        return self._text_storage.column
    
    @property
    def _current_char(self):
        return self._text_storage.current_char

    @property
    def _current_line(self):
        return self._text_storage.current_line

    def _set_current_token_and_skip(self, token):
        self._text_storage.skip(len(token))

        self._current_token = token
        return token
      
    def _process_eol(self):
        try:
            self._current_char
            return None
        except buffer.EOLError:
            self._text_storage.newline()

            return self._set_current_token_and_skip(
                token.Token(EOL, position=[self._text_storage.line, self._text_storage.column])
            )
          
    def _process_eof(self):
        try:
            self._current_line
            return None
        except buffer.EOFError:
            return self._set_current_token_and_skip(
                token.Token(EOF)
            )
            
    def _process_whitespace(self):
        regexp = re.compile(r"[^\S\r\n]+")

        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        self._text_storage.skip(len(match.group()))
        
    def _process_print(self):
        regexp = re.compile(r"\b(print\()")
        
        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        token_string = match.group()[:-1]

        return self._set_current_token_and_skip(
            token.Token(PRINT, token_string)
        ) 
        
    def _process_dfa(self):
        regexp = re.compile(r"\b(DFA\()")
        
        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        token_string = match.group()[:-1]

        return self._set_current_token_and_skip(
            token.Token(DFA, token_string)
        )
        
    def _process_nfa(self):
        regexp = re.compile(r"\b(NFA\()")
        
        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        token_string = match.group()[:-1]

        return self._set_current_token_and_skip(
            token.Token(NFA, token_string)
        )
        
    def _process_func_name(self):
        matches = self.func_names() 

        for i in matches:
            if i:         
                token_string = i.group()[:-1]

                return self._set_current_token_and_skip(
                    token.Token(FUNCTION_CALL, token_string)
                )
                
        return None
    
    def func_names(self, matches=None):
        if matches == None:
            matches = [] 
           
        regexp = re.compile(r"\b(open\()")
        matches.append(regexp.match(
            self._text_storage.tail
        ))
        
        regexp = re.compile(r"\b(save\()")
        matches.append(regexp.match(
            self._text_storage.tail
        ))
        
        regexp = re.compile(r"\b(test\()")
        matches.append(regexp.match(
            self._text_storage.tail
        ))
        
        regexp = re.compile(r"\b(definition\()")
        matches.append(regexp.match(
            self._text_storage.tail
        ))
        
        return matches
        
    def _process_boolean(self):
        regexp = re.compile(r"\b(True|False)\b")

        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        token_string = match.group()

        return self._set_current_token_and_skip(
            token.Token(BOOLEAN, token_string)
        ) 

    def _process_number(self):
        regexp = re.compile('\d+')

        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        token_string = match.group()

        return self._set_current_token_and_skip(
            token.Token(INTEGER, int(token_string))
        ) 
    
    def _process_string(self):
        regexp = re.compile(r"([\"\'])((?:\\\1|(?:(?!\1)).)*)(\1)")

        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        token_string = match.group()

        return self._set_current_token_and_skip(
            token.Token(STRING, token_string)
        )
        
    def _process_var(self):
        regexp = re.compile('[a-zA-Z_]+')
        
        match = regexp.match(
            self._text_storage.tail
        )
        
        if not match:
            return None
        
        token_string = match.group()
        
        return self._set_current_token_and_skip(
            token.Token(VAR, str(token_string))
        )
        
    def _process_literal(self):
        return self._set_current_token_and_skip(
            token.Token(LITERAL, self._current_char)
        )
        
    def discard(self, token):
        if self.get_token() != token:
            raise TokenError(
                'Expected token {}, found {}'.format(
                    token, self._current_token
                ))

    def discard_type(self, _type):
        t = self.get_token()

        if t.type != _type:
            raise TokenError(
                'Expected token of type {}, found {}'.format(
                    _type, self._current_token.type
                ))
