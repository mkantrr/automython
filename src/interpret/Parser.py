import interpret.Lexer as fa_lex
import interpret.Token as token

class Node:
    def asdict(self):
        return {}  # pragma: no cover
    
class PrintNode(Node):
    node_type = 'print_func'

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def asdict(self):
        return {
            'type': self.node_type,
            'to_print': self.variable,
            'value': self.value.asdict(),
        }
 
class BinaryNode(Node):
    node_type = 'binary'

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def asdict(self):
        result = {
            'type': self.node_type,
            'left': self.left.asdict()
        }

        result['right'] = None
        if self.right:
            result['right'] = self.right.asdict()

        result['operator'] = None
        if self.operator:
            result['operator'] = self.operator.asdict()

        return result
    
class AssignmentNode(Node):
    node_type = 'assignment'

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def asdict(self):
        return {
            'type': self.node_type,
            'variable': self.variable.value,
            'value': self.value.asdict(),
        }
        
class FunctionCallNode(Node):
    node_type = 'function_call'

    def __init__(self, variable, func_name, parameters):
        self.variable = variable
        self.func_name = func_name
        self.parameters = parameters

    def asdict(self):
        return {
            'type': self.node_type,
            'variable': self.variable.value,
            'function_name': self.func_name,
            'parameters': self.parameters.asdict(),
        }
        
class ValueNode(Node):
    node_type = 'value_node'

    def __init__(self, value):
        self.value = value

    def asdict(self):
        return {
            'type': self.node_type,
            'value': self.value
        }

class LiteralNode(ValueNode):
    node_type = 'literal'
    
class IntegerNode(ValueNode):
    node_type = 'integer'

    def __init__(self, value):
        self.value = int(value)
        
class BooleanNode(ValueNode):
    node_type = 'boolean'
    
    def __init__(self, value):
        if value == 'True':
            self.value = True
        else:
            self.value = False
            
    
class VariableNode(ValueNode):
    node_type = 'variable'
    
class StringNode(ValueNode):
    node_type = 'string'

    def __init__(self, value):
        self.value = str(value)
    
class DictionaryNode(ValueNode):
    node_type = 'dictionary'
    
    def __init__(self, dict):
        self.elements = dict
        for key, value in self.elements.items():
            self.key = key
            self.value = value
    def asdict(self):
        return {
            'type': self.node_type,
            'key':  self.key.asdict(), 
            'value': self.value.asdict()
        }
        
class CollectionNode(ValueNode):
    node_type = 'collection'
    
    def __init__(self, list):
        self.value = list
        self.elements = []
        for element in self.value:
            self.elements.append(element.asdict())
        
    def asdict(self):
        return {
            'type': self.node_type,
            'value': self.elements
        }

class ParametersNode(ValueNode):
    node_type = 'parameters'
    
    def __init__(self, list):
        self.value = list
        self.elements = []
        for element in self.value:
            self.elements.append(element.asdict())
        
    def asdict(self):
        return {
            'type': self.node_type,
            'value': self.elements
        }

class DFANode(ValueNode):
    node_type = 'dfa'
    
    def __init__(self, list):
        self.value = list
        self.elements = []
        for element in self.value:
            self.elements.append(element.asdict())
        
    def asdict(self):
        return {
            'type': self.node_type,
            'value': self.elements
        }
        
class NFANode(ValueNode):
    node_type = 'nfa'
    
    def __init__(self, list):
        self.value = list
        self.elements = []
        for element in self.value:
            self.elements.append(element.asdict())
        
    def asdict(self):
        return {
            'type': self.node_type,
            'value': self.elements
        }
        
class Parser:

    def __init__(self):
        self.lexer = fa_lex.Lexer()
        
    def _allow_whitespace(self):
        t = self.lexer.peek_token()
        while (t.type == fa_lex.EOL):
            self.lexer.discard_type(fa_lex.EOL)
            t = self.lexer.peek_token()
            
        return t
    
    def parse_print(self):
        t = self.lexer.get_token()
        
        if t.type != fa_lex.PRINT:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )
       
        return_node = None 
        with self.lexer:
            self._parse_literal(['('])
            node = PrintNode("print_func", self.parse_standalone_func())
            self._parse_literal([')'])
            return_node = node
            
        with self.lexer:
            self._parse_literal(['('])
            node = PrintNode("print_func", self.parse_function())
            self._parse_literal([')'])
            return_node = node
            
        with self.lexer: 
            self._parse_literal(['('])
            node = PrintNode("print_func", self.parse_collection())
            self._parse_literal([')'])
            return_node = node
            
        with self.lexer: 
            self._parse_literal(['('])
            node = PrintNode("print_func", self.parse_expression())
            self._parse_literal([')'])
            return_node = node
        
        with self.lexer:
            self._parse_literal(['('])
            self._parse_literal([')'])
            node = PrintNode("print_func", ParametersNode([]))
            return_node = node
            
        if not return_node:
            exception = fa_lex.SyntaxError(
                'Incorrect syntax for print() call at line {}'.format(
                    self.lexer.line
                )
            )
            return exception
        return return_node
    
    def parse_string(self):
        t = self.lexer.get_token()
        
        if t.type != fa_lex.STRING:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )
        
        return StringNode(t.value[1:len(t.value)-1])
    
    def parse_number(self):
        t = self.lexer.get_token()
        
        if t.type != fa_lex.INTEGER:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )

        if t.type == fa_lex.INTEGER:
            return IntegerNode(int(t.value))
        
    def parse_boolean(self):
        t = self.lexer.get_token()
        
        if t.type != fa_lex.BOOLEAN:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )

        if t.type == fa_lex.BOOLEAN:
            return BooleanNode(t.value)
    
    def _parse_variable(self):
        t = self.lexer.get_token()

        if t.type != fa_lex.VAR:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )

        return VariableNode(t.value)
    
    def parse_assignment(self):
        variable = self._parse_variable()
        self.lexer.discard(token.Token(fa_lex.LITERAL, '='))
       
        t = self.lexer.peek_token()
        func_t = self.lexer.peek_token(2)
        if func_t.type == fa_lex.LITERAL and func_t.value == '.':
            value = self.parse_function()
        elif t.type == fa_lex.DFA or t.type == fa_lex.NFA:
            value = self.parse_fa()
        elif t.type == fa_lex.LITERAL and t.value == '{':
            value = self.parse_collection()
        else:
            value = self.parse_expression()
            
        if not value or t == token.Token(fa_lex.EOL) or t == token.Token(fa_lex.EOF):
            raise fa_lex.SyntaxError(
                'Assignment has undefined value at line {}'.format(
                    t.value, self.lexer.line
                )
            )
           
        return AssignmentNode(variable, value)
    
    def _parse_func_name(self):
        t = self.lexer.get_token()
        
        if t.type != fa_lex.FUNCTION_CALL:
           raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )
        
        return StringNode(t.value)
    
    def _parse_func_parameters(self):
        t = self.lexer.peek_token() 
        if t.type != fa_lex.LITERAL and t.value != '(':
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )
        
        with self.lexer:
            self._parse_literal(['('])
            self._allow_whitespace()
            parameters = self.parse_parameters()
            self._allow_whitespace()
            self._parse_literal([')'])
            return ParametersNode(parameters)
        
    def parse_function(self):
        variable = self._parse_variable()
        self.lexer.discard(token.Token(fa_lex.LITERAL, '.'))
       
        t = self.lexer.peek_token()
        if t.type == fa_lex.FUNCTION_CALL:
            with self.lexer:
                function_name = self._parse_func_name()
            parameters = self._parse_func_parameters()
                
            if parameters:
                    return FunctionCallNode(variable, function_name, parameters)
            else:
                with self.lexer:
                    self._parse_literal(['('])
                    self._parse_literal([')']) 
                    return FunctionCallNode(variable, function_name, ParametersNode([]))
        else:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )
                
    def parse_standalone_func(self):
        t = self.lexer.peek_token()
        if t.type == fa_lex.FUNCTION_CALL:
            with self.lexer:
                function_name = self._parse_func_name()
            parameters = self._parse_func_parameters()
                
            if parameters:
                    return FunctionCallNode(StringNode("M"), function_name, parameters)
            else:
                with self.lexer:
                    self._parse_literal(['('])
                    self._parse_literal([')']) 
                    return FunctionCallNode(StringNode("M"), function_name, ParametersNode([]))
        else:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )
    
    def _parse_literal(self, values=None):
        t = self.lexer.get_token()

        if t.type != fa_lex.LITERAL:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )

        if values and t.value not in values:
            raise fa_lex.TokenError(
                'line {}, internal parsing failed, literal value not in parsable array'.format(
                    self.lexer.line
                )
            )

        return LiteralNode(t.value)
    
    def parse_factor(self):
        with self.lexer:
            self._parse_literal(['('])
            expression = self.parse_expression()
            self._parse_literal([')'])
            return expression
        
        with self.lexer:
            return self._parse_variable()
        
        t = self.lexer.peek_token()
        if t.type == fa_lex.INTEGER:
            return self.parse_number()
        elif t.type == fa_lex.BOOLEAN:
            return self.parse_boolean()
        else:
            return self.parse_string() 
        
        
    def parse_expression(self):
        left = self.parse_factor()

        with self.lexer:
            operator = self._parse_literal(['+'])
            right = self.parse_expression()

            left = BinaryNode(left, operator, right)
        
        if isinstance(left, fa_lex.TokenError) \
            or isinstance(left, fa_lex.SyntaxError):
                t = self.lexer.get_token()
                raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )
                
        return left 
    
    def parse_dictionary(self):
        key = self.parse_expression()
        
        with self.lexer:
            self.lexer.discard(token.Token(fa_lex.LITERAL, ':'))
            t = self._allow_whitespace() 
            if t.type == fa_lex.LITERAL and t.value == '{':
                value = self.parse_collection()
            else:
                value = self.parse_expression() 
                
            key = DictionaryNode({key: value})
            
        return key
         
    def parse_elements(self, collection=None):
        left = self.parse_dictionary() 
        if collection == None:
            collection = []     
        collection.append(left)
        
        with self.lexer:
            self._parse_literal([','])
            self._allow_whitespace() 
            collection = self.parse_elements(collection)
           
        return collection
    
    def parse_collection(self):
        t = self.lexer.peek_token()
        
        if t.type == fa_lex.LITERAL and t.value == '{':
            with self.lexer:
                self._parse_literal(['{'])
                self._allow_whitespace()
                collection = self.parse_elements()
                self._allow_whitespace()
                self._parse_literal(['}'])
                return CollectionNode(collection)
        else:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\' at line {}'.format(
                    t.value, self.lexer.line
                )
            )
       
    def parse_parameters(self, parameters=None):
        t = self.lexer.peek_token()
        if t.type == fa_lex.LITERAL and t.value == '{':
            left = self.parse_collection()
        else:
            left = self.parse_expression()
        if parameters == None:
            parameters = []     
        parameters.append(left)
        
        with self.lexer:
            self._parse_literal([','])
            self._allow_whitespace() 
            parameters = self.parse_parameters(parameters)
           
        return parameters   
        
    def parse_fa(self):
        t = self.lexer.get_token() 
        
        if t.type not in [fa_lex.DFA, fa_lex.NFA]:
            raise fa_lex.SyntaxError(
                'Unexpected value \'{}\', not a supported Automython FA at line {}'.format(
                    t.value, self.lexer.line
                )
            )
        
        if t.type == fa_lex.DFA:
            with self.lexer:
                self._parse_literal(['('])
                self._allow_whitespace()
                parameters = self.parse_parameters()
                self._allow_whitespace()
                self._parse_literal([')'])
                return DFANode(parameters) 
        else:
            with self.lexer:
                self._parse_literal(['('])
                self._allow_whitespace()
                parameters = self.parse_parameters()
                self._allow_whitespace()
                self._parse_literal([')'])
                return NFANode(parameters) 
            
    def parse_line(self):
        node = None
        
        with self.lexer:
            node = self.parse_standalone_func()
            
        with self.lexer:
            node = self.parse_print()
        
        with self.lexer:
            node = self.parse_assignment()
            
        if isinstance(node, fa_lex.TokenError) \
            or isinstance(node, fa_lex.SyntaxError):
            raise node
            
        with self.lexer:
            node = self.parse_function()
            
        with self.lexer:
            node = self.parse_expression()
            
        if isinstance(node, fa_lex.TokenError) \
            or isinstance(node, fa_lex.SyntaxError):
            raise node
        elif node:
            return node
        else:
            raise fa_lex.UnknownError(
                'line {}, the parsed node returned None'.format(
                    self.lexer.line
                )
            )