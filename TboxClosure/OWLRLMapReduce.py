__author__ = 'mpetyx'

from rdflib import BNode
from rdflib import Literal as rdflibLiteral
from rdflib import Namespace
from RDFClosure.RDFS import type
import functools

from RDFClosure.Literals import LiteralProxies

from RDFClosure.CombinedClosure import RDFS_OWLRL_Semantics


class OWLRLMapReduce(RDFS_OWLRL_Semantics):


    def closure(self):
        """
           Generate the closure the graph. This is the real 'core'.

           The processing rules store new triples via the L{separate method<store_triple>} which stores
           them in the L{added_triples<added_triples>} array. If that array is emtpy at the end of a cycle,
           it means that the whole process can be stopped.

           If required, the relevant axiomatic triples are added to the graph before processing in cycles. Similarly
           the exchange of literals against bnodes is also done in this step (and restored after all cycles are over).
        """
        self.pre_process()

        # Handling the axiomatic triples. In general, this means adding all tuples in the list that
        # forwarded, and those include RDF or RDFS. In both cases the relevant parts of the container axioms should also
        # be added.
        if self.axioms:
            self.add_axioms()

        # Create the bnode proxy structure for literals
        self.literal_proxies = LiteralProxies(self.graph, self)

        # Add the datatype axioms, if needed (note that this makes use of the literal proxies, the order of the call is important!
        if self.daxioms:
            self.add_d_axioms()

        self.flush_stored_triples()

        # Get first the 'one-time rules', ie, those that do not need an extra round in cycles down the line
        self.one_time_rules()
        self.flush_stored_triples()

        # Go cyclically through all rules until no change happens
        new_cycle = True
        cycle_num = 0
        while new_cycle:
            # yes, there was a change, let us go again
            cycle_num += 1

            # DEBUG: print the cycle number out
            if self._debug:
                print "----- Cycle #:%d" % cycle_num

            # go through all rules, and collect the replies (to see whether any change has been done)
            # the new triples to be added are collected separately not to interfere with
            # the current graph yet
            self.empty_stored_triples()

            # Execute all the rules; these might fill up the added triples array
            # for t in self.graph:
            #     self.rules(t, cycle_num)

            ############################################################################
            ############################################################################
            ############################################################################
            ####### MAP Function to improve Speed and extend it to MAP Reduce
            ############################################################################
            ############################################################################
            ############################################################################
            map(functools.partial(self.rules, cycle_num=cycle_num), self.graph)


            # closure = map(lambda triple:self.rules(triple,cycle_num), self.graph)

            # Add the tuples to the graph (if necessary, that is). If any new triple has been generated, a new cycle
            # will be necessary...
            new_cycle = len(self.added_triples) > 0
            if new_cycle:
                print "another more cycle ->"+str(cycle_num)

            for t in self.added_triples:
                self.graph.add(t)

        # All done, but we should restore the literals from their proxies

        self.literal_proxies.restore()

        self.post_process()

        self.flush_stored_triples()

        # Add possible error messages
        if self.error_messages:
            # I am not sure this is the right vocabulary to use for this purpose, but I haven't found anything!
            # I could, of course, come up with my own, but I am not sure that would be kosher...
            ERRNS = Namespace("http://www.daml.org/2002/03/agents/agent-ont#")
            self.graph.bind("err", "http://www.daml.org/2002/03/agents/agent-ont#")
            for m in self.error_messages:
                message = BNode()
                self.graph.add((message, type, ERRNS['ErrorMessage']))
                self.graph.add((message, ERRNS['error'], rdflibLiteral(m)))

