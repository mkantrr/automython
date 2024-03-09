#!/usr/bin/env python
import sys
import interpret.cli as cli
import interpret.file_interface as file

def interpret(argv=sys.argv):
  if len(argv) == 1:
    cli.cli()
  elif len(argv) == 2:
    if argv[1].lower().endswith('.theory'):
      file.interpret(argv[1])
    else:
      print('Wrong file type. Please pass in a .theory file, e.g.')
      print('automython <file-name>.theory')
      sys.exit(1)
  else:
    print('Invalid command.')
    sys.exit(1)

def main(filename=None):
  if not filename:
    cli.cli()
  else:
    file.interpret(filename)
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
      main()
    elif len(sys.argv) == 2:
      if sys.argv[1].lower().endswith('.theory'):
        main(sys.argv[1])
      else:
        sys.exit(1)
    else:
      sys.exit(1)