import interpret.helpers as helpers

class Visitor:
  def __init__(self):
      self.variables = {}
      self.printables = []
      self.DFAs = {}
      self.NFAs = {}
      self.DTMs = {}
      self.NTMs = {}
      self.MNTMs = {}
      
  def isvariable(self, name):
      return name in self.variables

  def valueof(self, name):
      if not self.isvariable(name):
          raise KeyError('SyntaxError: ' + name)
      return self.variables[name]['value']

  def typeof(self, name):
      if not self.isvariable(name):
          raise KeyError('SyntaxError: ' + name)
      return self.variables[name]['type']
  
  def visit(self, node):
    if node['type'] == 'integer':
        return node['value'], node['type']
    if node['type'] == 'boolean':
        return node['value'], node['type']
    if node['type'] == 'string':
        return node['value'], node['type']
    
    if node['type'] == 'variable':
        return self.valueof(node['value']), self.typeof(node['value'])

       
    if node['type'] == 'binary':
        lvalue, ltype = self.visit(node['left'])
        rvalue, rtype = self.visit(node['right'])

        operator = node['operator']['value']

        if operator == '+':
            return lvalue + rvalue, rtype
        
    if node['type'] == 'collection':
        is_dict = False
        for element in node['value']:
            if element['type'] == 'dictionary':
                is_dict = True
        if is_dict:
            collection = dict()
            for element in node['value']:
                if element['type'] == 'variable':
                    right_value, right_type = self.visit(element)
                    for key in right_value:
                         collection[key] = right_value[key]
                else:
                    right_key, right_value, right_type = self.visit(element)
                    collection[right_key] = right_value
            return collection, 'dictionary'
        else:
            collection = set()
            for element in node['value']:
                right_value, right_type = self.visit(element)
                collection.add(right_value)
            return collection, node['type']
    
    if node['type'] == 'parameters':
        collection = list()
        for element in node['value']:
            right_value, right_type = self.visit(element)
            collection.append(right_value)
        return collection, node['type']
  
    if node['type'] == 'dictionary':
        key_value, key_type = self.visit(node['key'])
        value_value, value_type = self.visit(node['value'])
        return key_value, value_value, node['type']
    
    if node['type'] == 'print_func':
        right_value, right_type = self.visit(node['value'])
        if type(right_value) == list and len(right_value) == 0:
            right_value = '' 
        self.printables.append(
            {node['to_print']: {
                'value': right_value,
                'type': right_type
            }
        })

        return None, None
    
    if node['type'] == 'function_call':
        right_parameters_value, right_parameters_type = self.visit(node['parameters'])
        function_name = node['function_name'].asdict()['value']
        default_file = node['variable'] + ".png"
        
        parameters = []
        if function_name not in ['open']:
            parameters.append(self.variables[node['variable']]['value'])
        if function_name in ['open', 'save']:
            if len(right_parameters_value) > 0:
                if str(right_parameters_value[0]).lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.pdf')):
                    default_file = right_parameters_value[0]
                    right_parameters_value.pop(0) 
            parameters.append(default_file)
            
        for i in right_parameters_value:
            parameters.append(i) 
            
        return getattr(helpers, function_name)(*parameters), node['type']
    
    if node['type'] == 'dfa':
        parameters = list()
        for element in node['value']:
            right_value, right_type = self.visit(element)
            parameters.append(right_value)
           
        try: 
            if len(parameters) == 6:
                parameters = helpers.make_DFA(
                                parameters[0],
                                parameters[1],
                                parameters[2],
                                parameters[3],
                                parameters[4],
                                parameters[5]
                            )
            else:
                parameters = helpers.make_DFA(
                                parameters[0],
                                parameters[1],
                                parameters[2],
                                parameters[3],
                                parameters[4],
                            )
        except Exception as e:
            print()
            print(str(e))
            return None, None
        
        return parameters, node['type']
    
    if node['type'] == 'nfa':
        parameters = list()
        for element in node['value']:
            right_value, right_type = self.visit(element)
            parameters.append(right_value)
           
        try: 
            parameters = helpers.make_NFA(
                parameters[0],
                parameters[1],
                parameters[2],
                parameters[3],
                parameters[4]
            )
        except Exception as e:
            print()
            print(str(e))
            return None, None
        
        return parameters, node['type']
        
    if node['type'] == 'assignment':
        right_value, right_type = self.visit(node['value'])
        if right_type == 'dfa':
            self.DFAs[node['variable']] = {
                'value': right_value,
                'type': right_type
            }
        if right_type == 'nfa':
            self.NFAs[node['variable']] = {
                'value': right_value,
                'type': right_type
            } 
        self.variables[node['variable']] = {
            'value': right_value,
            'type': right_type
        }

        return None, None