__author__ = 'mpetyx'

from TboxClosure.KBClosure import KnowledgeBaseClosure

from rdflib import ConjunctiveGraph

graph = ConjunctiveGraph().parse("pizza.ttl", format='turtle')


KnowledgeBaseClosure(graph=graph, axioms=True, daxioms=True).closure()

