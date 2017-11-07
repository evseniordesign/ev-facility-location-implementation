"""
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

def generate_coeffs(f_costs, c_costs):
    output = list(f_costs)
    output.extend(c_costs)
    return matrix(output)

def generateGH(f_len, c_len):
    num_customers = c_len / f_len
    outerlist = []
    h = []

    # -yi + xij
    for i in xrange(0, c_len):
        facility_num = i % f_len
        inner = []
        # -yi
        for j in xrange(0, f_len):
            if j == facility_num:
                inner.append(-1.0)
            else:
                inner.append(0.0)

        # xij
        for j in xrange(0, c_len):
            if j == i:
                inner.append(1.0)
            else:
                inner.append(0.0)
        
        h.append(0.0)
        outerlist.append(inner)

    # all >= 0
    for i in xrange(0, c_len + f_len):
        inner = []
        for j in xrange(0, c_len + f_len):
            if i == j:
                inner.append(-1.0)
            else:
                inner.append(0.0)

        h.append(0.0)
        outerlist.append(inner)

    # yi
    for i in xrange(0, f_len):
        inner = []
        for j in xrange(0, c_len + f_len):
            if i == j:
                inner.append(1.0)
            else:
                inner.append(0.0)

        h.append(1.0)
        outerlist.append(inner)

    return matrix(outerlist).trans(), matrix(h)

def generateAB(f_len, c_costs):
    num_customers = len(c_costs) / f_len
    outerlist = []
    b = []

    for x in xrange(0, num_customers):
        inner = []
        # facilities don't factor in here
        # zero out their coeffs
        for y in xrange(0, f_len):
            inner.append(0.0)
        for y in xrange(0, num_customers):
            # set one facility's variables to all 1's
            # everyone else's to all 0's
            # at the end, each facility has sum of their vars < 1
            for z in xrange(0, f_len):
                if(y == x):
                    inner.append(1.0)
                else:
                    inner.append(0.0)
        outerlist.append(inner)
        b.append(1.0)
    return matrix(outerlist).trans(), matrix(b)


def solve(f_costs, c_costs):
    c = generate_coeffs(f_costs, c_costs)
    A, b = generateAB(len(f_costs), c_costs)
    G, h = generateGH(len(f_costs), len(c_costs))
    sol = solvers.lp(c=c, G=G, h=h, A=A, b=b)
    return sol

def main():
    f_costs = [5.0, 2.0, 1.0] # 3 facilities
    c_costs = [3.0, 2.0, 3.0, 6.0, 1.0, 2.0] # 2 clients, c00, c10, c20, c01, etc.
    print solve(f_costs, c_costs)['x']

if __name__ == '__main__':
    main()
