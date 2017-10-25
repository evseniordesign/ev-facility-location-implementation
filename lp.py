"""

Our LP problem:
minimize sum of fi*yi  +  sum of cij*xij
sum of xij for all i = 1
xij <= yi
0 <= xij <= 1
0 <= yi <= 1

Constraints for G:
-yi + xij <= 0
xij <= 1
-xij <= 0
yi <= 1
-yi <= 0

Constraints for A:
sum of xij = 1

cvxopt format
minimize c(T)x  where c is the coefficients
Gx <= h
Ax = b 
"""
from cvxopt import matrix, solvers

def generate_coeffs(f_costs, c_costs):
    output = [x for x in f_costs]
    output.extend(c_costs)
    return matrix(output)

def generateG(f_len, c_len):
    outerlist = []
    for x in range(0, 5):
        inner = []
        for y in range(0, f_len):
            if(x == 0 or x == 4):
                inner.append(-1.0)
            elif(x == 3):
                inner.append(1.0)
            else:
                inner.append(0.0)
        for y in range(0, c_len):
            if(x == 0 or x == 1):
                inner.append(1.0)
            elif(x == 2):
                inner.append(-1.0)
            else:
                inner.append(0.0)
        outerlist.append(inner)
    return matrix(outerlist).trans()

def generateH():
    return matrix([0.0, 1.0, 0.0, 1.0, 0.0])

def generateA(f_len, c_costs):
    outerlist = []
    for x in range(0, len(c_costs)/f_len):
        inner = []
        for y in range(0, f_len):
            inner.append(0.0)
        for y in range(0, len(c_costs)/f_len):
            for z in range(0, f_len):
                if(y == x):
                    inner.append(1.0)
                else:
                    inner.append(0.0)
        outerlist.append(inner)
    return matrix(outerlist).trans()

def generateB(c_len):
    outerlist = []
    for x in range(0, c_len):
        outerlist.append([1.0])
    return matrix(outerlist).trans()

def main():
    f_costs = [5.0, 2.0] # 3 facilities
    c_costs = [3.0, 2.0, 3.0, 6.0] # 2 clients, c00, c10, c20, c01, etc.

    c = generate_coeffs(f_costs, c_costs)
    G = generateG(len(f_costs), len(c_costs))
    h = generateH()
    A = generateA(len(f_costs), c_costs)
    b = generateB(len(c_costs)/len(f_costs))
    print A, b

    sol = solvers.lp(c=c, G=G, h=h, A=A, b=b)

main()