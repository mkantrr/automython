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
```

## Testing functions

The following `.theory` code snippet creates a DFA and NFA variable and does various function calls and printing. The DFA accepts all words that end with '00' or '11', and the NFA accepts any word that has the substring '101' or '11' in it.

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

dfa.save()
dfa.save('dfa_wordcheck.png', '1011')

print(dfa.definition())
print()

print(dfa.test('1011'))
print()

print(open("dfa.png"))

nfa = NFA(
    {"s0", "s1", "s2", "s3"}, 
    {"0", "1", ""}, 
    {"s0": {"0": {"s0"}, "1": {"s0", "s1"}}, 
    "s1": {"0": {"s2"}, "": {"s2"}}, 
    "s2": {"1": {"s3"}}, 
    "s3": {"0": {"s3"}, "1": {"s3"}}}, 
    "s0", 
    {"s3"}
)
print(nfa)
print()

nfa.save()
nfa.save('nfa_wordcheck.png', '11')

print(nfa.definition())
print()

print(nfa.test('100101001'))
print()

print(open("nfa.png"))
```

