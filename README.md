AI---Constraint-Satisfaction-Problem

This program is the AI implemented to solve the Sudoko game using CSP (Constrained Satisfaction Problem) approach. Provided an initial board as a string in a file namely "sudokus_start.txt", program solves the puzzle within 1 minute and stores the result in "sudokus_finish.txt" file. It first uses AC3 algorithm to derive the feasible solution for every state. Then it applied backtracking using minimum remaining value and order domain with forward checking to come up with the final solution.
