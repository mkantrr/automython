import interpret.helpers as helpers

import interpret.Parser as fa_parse
import interpret.Lexer as fa_lex
import interpret.Visitor as fa_visitor

from IPython.display import display

def cli():
    parser = fa_parse.Parser()
    visitor = fa_visitor.Visitor()
   
    print('Automython 1.0 on ' + str(helpers.system_type())) 
    print('Enter/Paste your content. Ctrl-D (i.e. EOF) to end input block.')
    while True:
        text = ''
        while True:
            try:
                line = input('>>> ')
                if (line in ['exit', 'quit']):
                    print('Use exit() or quit() to exit.')
                    continue
                if (line in ['exit()', 'quit()']):
                    return
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print('\n'+'KeyboardInterrupt')
                continue
            
            text += line + '\n'
            
        if not text:
            continue

        parser.lexer.load(text)
        
        #print(parser.lexer.get_tokens())
        t = parser.lexer.peek_token()
        while (t.type != fa_lex.EOF):
            try:
                node = parser.parse_line()
                if node:
                    visitor.visit(node.asdict())
            except Exception as ex:
                print()
                template = "An exception of type {0} occurred:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                break
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
        
if __name__ == '__main__':
    cli()