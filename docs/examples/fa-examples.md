# FA Examples

This page hosts some examples of `.theory` syntax files that you can copy and paste and try yourself.

## Testing types

The following code snippet creates a few variables and prints them, as well as printing non-assigned values.
```python
integer = 123
print(integer)
print()

print(123)
print()

string = "s0"
print(string)
print()

print("s0")
print()

boolean = True
print(boolean)
print()

print(True)
print()

dict = {"s1": {"s2": 1}}
print(dict)
print()

print({"s1": {"s2": 1}})
print()

set = {"s1", "s2", "s3"}
print(set)
print()

print({"s1", "s2", "s3"})
print()

dfa = DFA(
  {'s0', "s1", 's2', "s3", "s4"}, 
  {"0", "1"}, 
  {"s0": {"0": "s3", "1": "s1"}, 
  "s1": {"0": "s3", "1": "s2"}, 
  "s2": {"0": "s3", "1": "s2"}, 
  "s3": {"0": "s4", "1": "s1"}, 
  "s4": {"0": "s4", "1": "s1"}}, 
  "s0", {"s2", "s4"}
)
print(dfa)
```

## Testing functions

The following code snippet creates a DFA variable and does various function calls and printing.

```python
dfa = DFA(
  {'s0', "s1", 's2', "s3", "s4"}, 
  {"0", "1"}, 
  {"s0": {"0": "s3", "1": "s1"}, 
  "s1": {"0": "s3", "1": "s2"}, 
  "s2": {"0": "s3", "1": "s2"}, 
  "s3": {"0": "s4", "1": "s1"}, 
  "s4": {"0": "s4", "1": "s1"}}, 
  "s0", {"s2", "s4"}
)
print(dfa)
print()

dfa.save('dfa.png')
dfa.save('dfa_wordcheck.png', '1011')

def = dfa.definition()
print(def)
print()

print(dfa.definition())
print()

test = dfa.test('1011')
print(test)
print()

print(dfa.test('1011'))
print()

print(open("dfa.png"))
```

