__author__ = 'mpetyx'

import functools

def apply_rules(triple, cycle):

    a,b,c = triple
    return (c,b,a)

triples = [ (1,2,3), (4,5,6), (7,8,9),(4,5,6), (1,2,3) ]

# Applying Rules
# closure = map(lambda x:apply_rules(x), triples)
closure = map(functools.partial(apply_rules, cycle=2), triples)


print closure

# Removing duplicates
final_closure = reduce(lambda x, y: x + y if y[0] not in x else x, map(lambda x: [x],closure))

print final_closure