from abc import abstractmethod
import copy
import itertools


class CSP:
    """
    Constraint Satisfaction Problem

    A general implementation that should be able to solve a variety of different CSP's.
    The documentation and comments do however sometimes use sudoku as an example.
    """

    def __init__(self):
        self.variables: list[str] = []
        # A domain consist of a variable and a list of possible values for that variable
        self.domains: dict[str, list] = {}
        # self.constraints[i][j] is a list of legal value pairs for the variable pair (i, j)
        self.constraints: dict = {}

        self.counter_backtrack_calls: int = 0
        self.counter_backtrack_fails: int = 0

    def add_variable(self, name: str, possible_values: list):
        """Add a new variable to the CSP.

        Args:
            'name': The variable name, in sudoku this could be `'row-col'`.

            'domain': A list of the legal values for the variable. (sudoku: 1-9 for unknown values)
        """
        self.variables.append(name)
        self.domains[name] = possible_values
        self.constraints[name] = {}

    def _get_all_possible_pairs(self, a: list, b: list) -> list:
        """
        Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def _get_all_arcs(self) -> list:
        """
        Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def _get_all_neighboring_arcs(self, var) -> list:
        """
        Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, x: str, y: str, filter_function):
        """
        Add a new constraint between variables `i` and `j`. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not y in self.constraints[x]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[x][y] = self._get_all_possible_pairs(
                self.domains[x], self.domains[y])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[x][y] = list(
            filter(lambda value_pair: filter_function(
                *value_pair), self.constraints[x][y])
        )

    def add_all_different_constraint(self, variables):
        """
        Add an All-diff constraint between all of the variables in the
        list 'variables'. (none of these variable can have the same value)
        """
        for (x, y) in self._get_all_possible_pairs(variables, variables):
            if x != y:
                self.add_constraint_one_way(x, y, lambda a, b: a != b)

    def backtracking_search(self):
        """
        This functions starts the CSP solver and returns the found
        solution.
        """
        # deep copy is required to ensure that any changes made to 'assignment'
        # does not have any side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self._inference(assignment, self._get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self._backtrack(assignment)

    def _backtrack(self, domains: dict) -> dict:
        """
        The function is called recursively, with a partial assignment of
        values 'assignment'.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        If a value choice leads to failure (noticed either by
        INFERENCE or by BACKTRACK), then value assignments (including those
        made by INFERENCE) are retracted and a new value is tried.

        Args:
            `domains` (dict): A dictionary that contains
            a list of all legal values for the variables that have *not* yet
            been decided, and a list of only a single value for the
            variables that *have* been decided.
        """
        self.counter_backtrack_calls += 1

        # get next variable
        next_variable = self._select_unassigned_variable(domains)

        if next_variable is None:
            # No more variable to check
            return domains

        for possible_value in domains[next_variable]:
            assignment_copy = copy.deepcopy(domains)
            assignment_copy[next_variable] = [possible_value]

            if self._inference(assignment_copy, self._get_all_arcs()):
                result = self._backtrack(assignment_copy)
                if result:
                    return result

        self.counter_backtrack_fails += 1

    def _select_unassigned_variable(self, domains: dict) -> str:
        """
        Returns the name of one of the variables in 'domains' that have not yet been decided, i.e. whose list of legal values has a length greater than one.
        """
        for variable in domains:
            # Check if variable has legal values
            if len(domains[variable]) > 1:
                # Return first variable that does
                return variable

    def _inference(self, domains: dict, queue: list) -> bool:
        """
        The function 'AC-3' (inference) from the pseudocode in the textbook.

        Args:
            domains (`dict`): The current partial assignment, that contains the lists of legal values for each undecided variable. 
            queue (`list`): The initial queue of arcs that should be visited.

        Returns:
             `bool`: False if an inconsistency is found and True otherwise
        """
        while queue:  # while queue is not empty
            x, y = queue.pop()

            if self._revise(domains, x, y):

                if len(domains[x]) == 0:
                    # No legal values left for x
                    # this means
                    return False

                for arc in self._get_all_neighboring_arcs(x):
                    if arc not in queue:
                        queue.append(arc)
        return True

    def _revise(self, domains: list, x: str, y: str) -> bool:
        """
        If a value is found in variable i's domain that doesn't satisfy 
        the constraint between i and j, the value should be deleted from 
        i's list of legal values in `assignment`.

        Args:
            `domains`: The current partial assignment, that contains the lists of legal values for each undecided variable. 
            `x` and `y`: specifies the arc that should be visited. 

        Returns:
            `bool`: wether the assignment was revised or not
        """
        was_revised = False

        for i in domains[x]:

            i_satisfies_a_constraint_with_j = False
            for j in domains[y]:
                if (i, j) in self.constraints[x][y]:
                    i_satisfies_a_constraint_with_j = True

            if not i_satisfies_a_constraint_with_j:
                # remove x because it has no valid constraint
                domains[x].remove(i)
                was_revised = True

        return was_revised
