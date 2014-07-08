__author__ = 'mpetyx'

"""

A parent is a sublclass of a person who has at least one child
"""


from rdflib import Graph
from TboxClosure.KBClosure import KnowledgeBaseClosure


graph = Graph().parse(source="sample.ttl", format="turtle")
print len(graph)

KnowledgeBaseClosure(graph=graph, axioms=True, daxioms=True).closure()

graph.serialize("test.ttl", format="turtle")
