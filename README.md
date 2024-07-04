# CKY-parsing

This project was completed for the course Natural Language Processing in Columbia University.

Project goals: 
- implement the CKY (Cocke–Younger–Kasami) algorithm for CFG (Context Free Grammar) and PCFG (Probabilistic CFG) parsing.
- retrieve parse trees from a parse chart to practice working with tree data structures

In `grammar.py`:
- `verify_grammar()`: checks that the grammar is a valid PCFG in CNF
- main section reads in the grammar, print out a confirmation if the grammar is a valid PCFG in CNF or print an error message if it is not

In `cky.py`:
- `is_in_language(self, tokens)`: implements the CKY algorithm. Reads in a list of tokens and returns True if the grammar can parse the sentence and False if otherwise.
- `parse_with_backpointers(self, tokens)`: retrieve the most probable parse for the input sentence, given the PCFG probabilities in the grammar.
- `get_tree(chart, i,j, nt)`: returns the parse-tree rooted in non-terminal nt and covering span i,j.
