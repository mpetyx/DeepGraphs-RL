__author__ = 'mpetyx'


from rdflib.graph import Graph
from StringIO import StringIO

RULES = \
"""
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix : <http://www.w3.org/2002/07/koukli#>.


{ ?x owl:sameAs ?y } => { ?y owl:sameAs ?x } .
# { ?x owl:sameAs ?y . ?x ?p ?o } => { ?y ?p ?o } .
{ ?X owl:sameAs ?A . ?A owl:sameAs ?B } => { ?X owl:sameAs ?B } .

{ ?x1 :hasParent ?x2 . ?x2 :hasBrother ?x3 . } =>  { ?x1 :hasUncle ?x3 }.
"""

"""
# Person(?p), hasAge(?p, ?age), greaterThan(?age, 18) -> Adult(?p)

{ ?p rdf:type :Person. ?p :hasAge ?age. ?age swrl:greaterThan 18.} => {?p rdf:type :Adult.}
"""

graph = Graph().parse(StringIO(RULES), format="n3")

for triple in graph:
    for t in triple:
        print t

print "the graph length is",len(graph)

print(graph.serialize(format='json-ld', indent=4))