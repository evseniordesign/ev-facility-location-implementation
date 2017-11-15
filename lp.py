"""
This module interfaces with cvxopt to produce the optimal solution for the LP.

Our LP problem:
minimize sum of fi*yi  +  sum of cij*xij
sum of xij for all i = 1
xij <= yi
0 <= xij <= 1
0 <= yi <= 1

Constraints for G:
-yi + xij <= 0
-xij <= 0
-yi <= 0
yi <= 1

Constraints for A:
sum of xij = 1

cvxopt format
minimize c(T)x  where c is the coefficients
Gx <= h
Ax = b
"""

from cvxopt import matrix, solvers
solvers.options['show_progress'] = False

def generate_coeffs(f_costs, c_costs):
    """
    Generates the maximization equation for the LP.
    """
    output = list(f_costs)
    output.extend(c_costs)
    return matrix(output)

def generate_gh(f_len, c_len):
    """
    Generates the 'less than' constraints for the LP.
    """
    outerlist = []
    result = []

    # -yi + xij
    for i in xrange(0, c_len):
        facility_num = i % f_len
        inner = []
        # -yi
        for j in xrange(0, f_len):
            inner.append(-1.0 if j == facility_num else 0.0)

        # xij
        for j in xrange(0, c_len):
            inner.append(1.0 if j == facility_num else 0.0)

        result.append(0.0)
        outerlist.append(inner)

    # all >= 0
    for i in xrange(0, c_len + f_len):
        inner = []
        for j in xrange(0, c_len + f_len):
            inner.append(-1.0 if i == j else 0.0)

        result.append(0.0)
        outerlist.append(inner)

    # yi
    for i in xrange(0, f_len):
        inner = []
        for j in xrange(0, c_len + f_len):
            inner.append(1.0 if i == j else 0.0)

        result.append(1.0)
        outerlist.append(inner)

    return matrix(outerlist).trans(), matrix(result)

def generate_ab(f_len, c_costs):
    """
    Generates the 'equal to' constraints for the LP.
    """
    num_customers = len(c_costs) / f_len
    outerlist = []
    results = []

    for row_num in xrange(0, num_customers):
        inner = []
        # facilities don't factor in here
        # zero out their coeffs
        for _ in xrange(0, f_len):
            inner.append(0.0)
        for curr_customer in xrange(0, num_customers):
            # set one facility's variables to all 1's
            # everyone else's to all 0's
            # at the end, each facility has sum of their vars < 1
            for _ in xrange(0, f_len):
                # set value f_len times to go through one customer's vars
                inner.append(1.0 if row_num == curr_customer else 0.0)

        outerlist.append(inner)
        results.append(1.0)
    return matrix(outerlist).trans(), matrix(results)

def solve(f_costs, c_costs):
    """
    Combines all constraints and sends the LP to the solver.
    """
    coeffs = generate_coeffs(f_costs, c_costs)
    eq_mat, eq_vec = generate_ab(len(f_costs), c_costs)
    lt_mat, lt_vec = generate_gh(len(f_costs), len(c_costs))
    sol = solvers.lp(c=coeffs, G=lt_mat, h=lt_vec, A=eq_mat, b=eq_vec)
    return sol
