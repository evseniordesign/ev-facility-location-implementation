"""
Assign output colors to each power line based on load.
Main function is color_powerlines, rest are helpers.
"""
from collections import defaultdict
import Queue

YELLOW_LIMIT = 0.85
GREEN_LIMIT = 0.7

CAPACITIES = defaultdict(
    lambda: 10000, # default value
    residential=5000,
    commercial=40000,
    substation=50000,
)


def is_adjacent(line1, line2):
    """
    Check if two lines are adjacent.
    """
    return \
        line1['startlat'] == line2['startlat'] and line1['startlong'] == line2['startlong'] or \
        line1['startlat'] == line2['endlat'] and line1['startlong'] == line2['endlong'] or \
        line1['endlat'] == line2['startlat'] and line1['endlong'] == line2['startlong'] or \
        line1['endlat'] == line2['endlat'] and line1['endlong'] == line2['endlong']

def num_to_color(num, capacity):
    """
    Convert a number of EVs using a line and capacity of that line
    into a color to be displayed on the map.
    """
    if capacity * YELLOW_LIMIT < num:
        return 'red'
    elif capacity * GREEN_LIMIT < num:
        return 'yellow'
    else:
        return 'green'

def search_for_substation(start, adj_list, powerlines):
    """
    Search for the substation that start is connected to and return the path.
    """
    visited = set()
    bfs_q = Queue.Queue()

    # Used to reconstruct path
    parents = dict()

    # Find where to start in powerlines graph, where "start" is connected to
    for line in powerlines:
        if start['long'] == line['startlong'] and start['lat'] == line['startlat'] or \
                start['long'] == line['endlong'] and start['lat'] == line['endlat']:
            bfs_q.put(line['index'])
            break
    else:
        # this start node isn't connected
        return []

    # BFS for substation
    while not bfs_q.empty():
        curr = bfs_q.get()

        # Path found, backtrack and return path
        if powerlines[curr]['type'].lower().strip() == 'substation':
            path = [powerlines[curr]]
            while curr in parents.keys():
                curr = parents[curr]
                path.append(powerlines[curr])

            return path

        visited.add(curr)
        for index in adj_list[curr]:
            if index not in visited:
                bfs_q.put(index)
                parents[index] = curr

    # no path found
    return []

def color_powerlines(data, output):
    """
    Add colors for the powerlines before and after facility assignment.
    """
    for index, line in enumerate(data['powerlines']):
        # store number of evs using the line for now
        # will be replaced by colors later
        line['beforecolor'] = 0
        line['aftercolor'] = 0
        line['index'] = index
        line['capacity'] = CAPACITIES[line['type'].lower().strip()]

    # Adjacency list modeling powerline graph
    adj_list = [[line1['index']
                 for line1 in data['powerlines']
                 if is_adjacent(line1, line2) and line1['index'] != line2['index']]
                for line2 in data['powerlines']]

    # search for a substation
    # Anything along the path is "used" by this EV user
    # Keep a running count of people using each line

    # before colors
    for client in data['clients']:
        path = search_for_substation(client, adj_list, data['powerlines'])
        for line in path:
            line['beforecolor'] += float(client['population'])

    # after colors
    for facility in output.keys():
        if 'dummy' in facility:
            for client in output[facility]:
                path = search_for_substation(facility, adj_list, data['powerlines'])
                for line in path:
                    line['aftercolor'] += float(client['population'])
        else:
            path = search_for_substation(facility, adj_list, data['powerlines'])
            for line in path:
                line['aftercolor'] += sum(float(client['population'])
                                          for client in output[facility])

    # convert numbers to colors
    for line in data['powerlines']:
        line['aftercolor'] = num_to_color(line['aftercolor'], line['capacity'])
        line['beforecolor'] = num_to_color(line['beforecolor'], line['capacity'])
