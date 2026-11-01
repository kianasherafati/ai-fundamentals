import sys
from crossword import *

class Creator():

    def __init__(self, crossword, heuristic=True):
        '''
        initializes new crossword to inherit from crossword class
        also initializes domain for each variable
        '''
        self.crossword = crossword
        self.heuristic = heuristic # Determines if heuristics like MRV/LCV should be used
        self.domains = {}
        for var in self.crossword.variables:
            self.domains[var] = self.crossword.words.copy()

    def is_domain_consistent(self):
        """
        Enforce node consistency by removing words whose length != variable length.
        """
        for var in self.domains:
            for word in set(self.domains[var]):
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Revise domain of x to enforce consistency with y.
        Remove any word from domain[x] that has no matching word in domain[y]
        based on the overlapping character.
        """
        revised = False
        overlap = self.crossword.overlaps.get((x, y))

        if overlap is None:
            return False

        i, j = overlap

        for x_word in set(self.domains[x]):
            match_found = False
            for y_word in self.domains[y]:
                if x_word[i] == y_word[j]:
                    match_found = True
                    break
        
            if not match_found:
                self.domains[x].remove(x_word)
                revised = True

        return revised

    def pre_process_ac3(self):
        """
        Generates the initial queue of arcs for AC-3.
        An arc is a tuple (x, y) for all neighboring variables.
        """
        arcs = list()
        for x in self.domains:
            for y in self.crossword.neighbours(x):
                arcs.append((x, y))
        return arcs

    def ac3(self, arcs=None):
        """
        Implement AC-3 algorithm to enforce arc consistency.
        Should return True if successful; False if a domain becomes empty.
        """
        if arcs is None:
            arcs = self.pre_process_ac3()

        while arcs:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                
             
                for z in self.crossword.neighbours(x):
                    if z != y:
                        arcs.append((z, x))
        return True

    def is_assign_consistent(self, assignment):
        """
        Check if a given assignment is consistent.
        1. All words must be distinct.
        2. All words must satisfy node consistency (length).
        3. All words must satisfy arc consistency (overlaps).
        """
        # 1. Distinct values check
        words = list(assignment.values())
        if len(words) != len(set(words)):
            return False

        for var, word in assignment.items():
            # 2. Node consistency check (Length)
            if var.length != len(word):
                return False

            # 3. Arc consistency check (Overlaps)
            for neighbor in self.crossword.neighbours(var):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        i, j = overlap
                        if word[i] != assignment[neighbor][j]:
                            return False
        return True

    def is_solved(self, assignment):
        '''
        Helper function to show whether the crossword is complete
        '''
        return not bool(self.crossword.variables - set(assignment))

    def select_unassigned_var(self, assignment, heuristic=True):
        """
        Select an unassigned variable.
        If heuristic is True:
            1. MRV: Minimum Remaining Values in domain.
            2. Degree Heuristic: Largest degree (most neighbors) as tie-breaker.
        Else:
            Return the first available unassigned variable.
        """
        unassigned = [v for v in self.crossword.variables if v not in assignment]

        if not heuristic:
            return unassigned[0]

      
        
        return sorted(unassigned, key=lambda var: (
            len(self.domains[var]), 
            -len(self.crossword.neighbours(var))
        ))[0]

    def order_domain_values(self, var, assignment):
        """
        Return domain values for `var` ordered by Least Constraining Value (LCV).
        The LCV heuristic prefers values that eliminate the fewest options
        for neighboring variables.
        """
        values = list(self.domains[var])
        
    
        if not self.heuristic:
            return values

        def count_constraints(value):
            count = 0
            for neighbor in self.crossword.neighbours(var):
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        i, j = overlap
                        for neighbor_word in self.domains[neighbor]:
                            if value[i] != neighbor_word[j]:
                                count += 1
            return count

      
        return sorted(values, key=count_constraints)

    def backtrack(self, assignment):
        """
        Implement recursive backtracking search.
        Should return a complete assignment if successful, else None.
        """
       
        if self.is_solved(assignment):
            return assignment

        var = self.select_unassigned_var(assignment, self.heuristic)

        
        for value in self.order_domain_values(var, assignment):
         
            new_assignment = assignment.copy()
            new_assignment[var] = value

            if self.is_assign_consistent(new_assignment):
                
    
                
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result


        return None

    def solve(self):
        """
        Solve the crossword CSP by enforcing consistency and using backtracking search.
        """
        self.is_domain_consistent()
        if not self.ac3():
            return None 
        return self.backtrack(dict())