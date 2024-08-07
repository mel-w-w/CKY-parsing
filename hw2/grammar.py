"""

Melissa Marie Wang
msw2178

COMS W4705 - Natural Language Processing - Summer 2022
Homework 2 - Parsing with Context Free Grammars
Daniel Bauer
"""

import sys
from collections import defaultdict
import math
from math import fsum


class Pcfg(object):
    """
    Represent a probabilistic context free grammar.
    """

    def __init__(self, grammar_file):
        self.rhs_to_rules = defaultdict(list)
        self.lhs_to_rules = defaultdict(list)
        self.startsymbol = None
        self.read_rules(grammar_file)

    def read_rules(self, grammar_file):

        for line in grammar_file:
            line = line.strip()
            if line and not line.startswith("#"):
                if "->" in line:
                    rule = self.parse_rule(line.strip())
                    lhs, rhs, prob = rule
                    self.rhs_to_rules[rhs].append(rule)
                    self.lhs_to_rules[lhs].append(rule)
                else:
                    startsymbol, prob = line.rsplit(";")
                    self.startsymbol = startsymbol.strip()

    def parse_rule(self, rule_s):
        lhs, other = rule_s.split("->")
        lhs = lhs.strip()
        rhs_s, prob_s = other.rsplit(";", 1)
        prob = float(prob_s)
        rhs = tuple(rhs_s.strip().split())
        return (lhs, rhs, prob)

    def verify_grammar(self):
        """
        Return True if the grammar is a valid PCFG in CNF.
        Otherwise return False.
        """

        # Condition 1: all nonterminals must be uppercase.
        nonterminals_list = []

        for key in self.lhs_to_rules.keys():
            nonterminals_list.append(key)

        for nonterminal in nonterminals_list:
            if(nonterminal.isupper() != True):
                 # fails the 1st condition :(
                return False
            else:
                # passed the first condition :)
                # Condition 2: All probabilities of a key must sum up to 1
                for key in self.lhs_to_rules.keys():
                    probabilities = [list[2] for list in self.lhs_to_rules[key]]
                    added_probs = sum(probabilities)
                    if(math.isclose(added_probs, 1.0) != True):
                        # fails the 2nd condition :(
                        return False 
                    else:
                        # hooray! Grammar is verified!
                        return True
        



if __name__ == "__main__":
    with open(sys.argv[1],'r') as grammar_file:
     grammar = Pcfg(grammar_file)
    
     grammar.verify_grammar()

     if(grammar.verify_grammar()):
        print("Hooray! Your grammar is verified!")
     else:
        print("Oh nawr! Your grammar is NOT verified.")
        

