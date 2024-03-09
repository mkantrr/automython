import interpret.Parser as fa_parse
import interpret.Lexer as fa_lex
import interpret.Visitor as fa_visitor

import sys

from IPython.display import display

def interpret(filename):
  parser = fa_parse.Parser()
  visitor = fa_visitor.Visitor()
  error_flag = True
   
  text = ''
  
  try:
    all_lines = open(filename, "r").read().splitlines()
    
    for line in all_lines:
      if line:
        line = ''.join(line.split())
        text += line + '\n'
      else:
        text += '\n'
        
    parser.lexer.load(text)
    
    #print(parser.lexer.get_tokens())
     
    t = parser.lexer.peek_token()
    while (t.type != fa_lex.EOF):
      node = parser.parse_line()
      if node:
        visitor.visit(node.asdict())
      t = parser.lexer.peek_token()
      if (t.type == fa_lex.EOL):
        t = parser.lexer.get_token()
        t = parser.lexer.peek_token()
        while (t.type == fa_lex.EOL):
          if t.type == fa_lex.EOL:
            t = parser.lexer.get_token()
          t = parser.lexer.peek_token()
        
    for i in visitor.printables:
      if type(i['print_func']['value']) == tuple:
        if i['print_func']['value'][1] == 'ipython_display':
          display(i['print_func']['value'][0])
      else:
        print(i['print_func']['value'])
    visitor.printables = []
          
    error_flag = False
    
  except EOFError:
    sys.exit(0)
  
  except Exception as ex:
    print()
    template = "An exception of type {0} occurred:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    
  if error_flag:
    sys.exit(1)
    
if __name__ == '__main__':
  if len(sys.argv) == 2 and sys.argv[1].lower().endswith('.theory'):
    interpret(sys.argv[1])
  else:
    print('No file provided. Please pass in a .theory file, e.g.')
    print('python3 <path-to-file_interface.py> <file-name>.theory')
