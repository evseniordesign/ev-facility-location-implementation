"""
Temporary test file to run the algorithm code.
"""

from facility_location.algorithm import choose_facilities

def from_file(filename):
    """
    Initializes the graph from the given file.
    """
    infofile = open(filename)
    lengths = infofile.readline().split()
    num_facilities = int(lengths[0])
    num_clients = int(lengths[1])

    fcosts = map(float, infofile.readline().split())
    ccosts = None

    try:
        for _ in xrange(0, num_clients):
            client = map(float, infofile.readline().split())
            if ccosts is None:
                ccosts = [client]
            else:
                ccosts.append(client)
            if len(client) != num_facilities:
                raise ValueError()
    except ValueError:
        print "_fcosts and _ccosts must contain f_len values."
        exit(1)

    infofile.close()
    return fcosts, ccosts

def main():
    """
    Driver for the algorithm solver.
    """
    fcosts, ccosts = from_file('test.txt')
    print choose_facilities(fcosts, ccosts)
    print choose_facilities(fcosts, ccosts, "det_round")

if __name__ == '__main__':
    main()
