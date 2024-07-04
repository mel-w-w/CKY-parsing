"""

Melissa Marie Wang
msw2178

COMS W4705 - Natural Language Processing - Summer 2022
Homework 2 - Parsing with Probabilistic Context Free Grammars
Daniel Bauer

"""
import math
import sys
from collections import defaultdict
import itertools
from grammar import Pcfg


### Use the following two functions to check the format of your data structures in part 3 ###


def check_table_format(table):
    """
    Return true if the backpointer table object is formatted correctly.
    Otherwise return False and print an error.
    """
    if not isinstance(table, dict):
        sys.stderr.write("Backpointer table is not a dict.\n")
        return False
    for split in table:
        if not isinstance(split, tuple) and len(split) == 2 and \
                isinstance(split[0], int) and isinstance(split[1], int):
            sys.stderr.write(
                "Keys of the backpointer table must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write(
                "Value of backpointer table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str):
                sys.stderr.write(
                    "Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            bps = table[split][nt]
            if isinstance(bps, str):  # Leaf nodes may be strings
                continue
            if not isinstance(bps, tuple):
                sys.stderr.write(
                    "Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Incorrect type: {}\n".format(bps))
                return False
            if len(bps) != 2:
                sys.stderr.write(
                    "Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Found more than two backpointers: {}\n".format(bps))
                return False
            for bp in bps:
                if not isinstance(bp, tuple) or len(bp) != 3:
                    sys.stderr.write(
                        "Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has length != 3.\n".format(bp))
                    return False
                if not (isinstance(bp[0], str) and isinstance(bp[1], int) and isinstance(bp[2], int)):
                    print(bp)
                    sys.stderr.write(
                        "Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has incorrect type.\n".format(bp))
                    return False
    return True


def check_probs_format(table):
    """
    Return true if the probability table object is formatted correctly.
    Otherwise return False and print an error.
    """
    if not isinstance(table, dict):
        sys.stderr.write("Probability table is not a dict.\n")
        return False
    for split in table:
        if not isinstance(split, tuple) and len(split) == 2 and isinstance(split[0], int) and isinstance(split[1], int):
            sys.stderr.write(
                "Keys of the probability must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write(
                "Value of probability table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str):
                sys.stderr.write(
                    "Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            prob = table[split][nt]
            if not isinstance(prob, float):
                sys.stderr.write(
                    "Values of the inner dictionary (for each span and nonterminal) must be a float.{}\n".format(prob))
                return False
            if prob > 0:
                sys.stderr.write(
                    "Log probability may not be > 0.  {}\n".format(prob))
                return False
    return True


class CkyParser(object):
    """
    A CKY parser.
    """

    def __init__(self, grammar):
        """
        Initialize a new parser instance from a grammar.
        """
        self.grammar = grammar

    def is_in_language(self, tokens):
        """
        Membership checking. Parse the input tokens and return True if
        the sentence is in the language described by the grammar. Otherwise
        return False
        """
        # TODO, part 2

        # Goal: code the CKY algorithm

        # make the parse table using a set
        n = len(tokens)
        pi_table = {}

        # iterate through the length of s to make the table
        for i in range(n):
            j = i + 1

            # we're p much making a dictionary
            pi_table[(i, j)] = self.grammar.rhs_to_rules[(tokens[i],)]

        # main loop
        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length

                pi_table[(i, j)] = []

                # M
                for k in range(i + 1, j):
                    for b in pi_table[(i, k)]:
                        for c in pi_table[(k, j)]:

                            pi_table[(i, j)] = pi_table[(i, j)] + \
                                self.grammar.rhs_to_rules[(b[0], c[0])]

        # return the boolean True if the input string can be parsed
        for rule in pi_table[0, n]:
            if rule[0] == "TOP":
                return True

        return False

    def parse_with_backpointers(self, tokens):
        """
        Parse the input tokens and return a parse table and a probability table.
        """
       
        table = {}
        probs = {}

        n = len(tokens)

        # iterate through the length of s to make the table
        for i in range(n):
            j = i + 1

            # 2D dictionaries
            table[(i, j)] = {}
            probs[(i, j)] = {}

            # we're p much making a dictionary
            for rule in self.grammar.rhs_to_rules[(tokens[i],)]:
                table[(i, j)][rule[0]] = tokens[i]
                probs[(i, j)][rule[0]] = math.log2(rule[2])

        # main loop
        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length

                table[(i, j)] = {}
                probs[(i, j)] = {}

                # M
                for k in range(i + 1, j):
                    for b in table[(i, k)]:
                        for c in table[(k, j)]:

                            for rule in self.grammar.rhs_to_rules[(b, c)]:

                                # you need the biggest probability and the probabilities of its daughters
                                new_probability = math.log2(rule[2]) + probs[(i, k)][rule[1][0]] + probs[(k, j)][rule[1][1]]

                                if rule[0] not in probs[(i, j)] or new_probability > probs[(i, j)][rule[0]]:
                                    table[(i, j)][rule[0]] = (
                                        (rule[1][0], i, k), (rule[1][1], k, j))
                                    # new_probability was better!
                                    probs[(i, j)][rule[0]] = new_probability

                            

        if "TOP" not in table[0, n]:
            return None, None

        return table, probs

       


def get_tree(chart, i, j, nt):
    """
    Return the parse-tree rooted in non-terminal nt and covering span i,j.
    """
   
    # Look for TOP
    # Keep looking at all the children
    # Print the entire family tree
    
    cell = chart[(i,j)][nt]

    if j == i + 1:
        return (nt, cell)
    else:
        return (nt, get_tree(chart, cell[0][1], cell[0][2], cell[0][0]), get_tree(chart, cell[1][1], cell[1][2], cell[1][0]))



if __name__ == "__main__":

    with open('atis3.pcfg','r') as grammar_file:
        grammar = Pcfg(grammar_file)
        
        print(grammar.verify_grammar())

        parser = CkyParser(grammar)

        toks =['flights', 'from','miami', 'to', 'cleveland','.']

    print(parser.is_in_language(toks))
    table,probs = parser.parse_with_backpointers(toks)
    assert check_table_format(table)
    assert check_probs_format(probs)
    print("Done running!")

