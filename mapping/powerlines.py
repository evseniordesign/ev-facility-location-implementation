YELLOW_LIMIT = 0.85
GREEN_LIMIT = 0.7

import Queue

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
    if capacity * YELLOW_LIMIT > num:
        return 'red'
    elif capacity * GREEN_LIMIT > num:
        return 'yellow'
    else:
        return 'green'

def search_for_substation(start, adj_list, powerlines):
    """
    Search for the substation that start is connected to and return the path.
    """
    visited = set()
    parents = dict()
    bfs_q = Queue.Queue()

    for line in powerlines:
        if start['long'] == line['startlong'] and start['lat'] == line['startlat'] or \
                start['long'] == line['endlong'] and start['lat'] == line['endlat']:
            bfs_q.put(line)
            break
    else:
        # this start node isn't connected
        return []

    while not bfs_q.empty():
        curr = bfs_q.get()

        if powerlines[curr]['type'] == 'substation':
            path = [curr]
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
    powerlines = data['powerlines']

    for index, line in enumerate(powerlines):
        # store number of evs using the line for now
        # will be replaced by colors later
        line['index'] = index
        line['beforecolor'] = 0
        line['aftercolor'] = 0

    adj_list = [[line1['index']
                 for line1 in powerlines if is_adjacent(line1, line2)]
                for line2 in powerlines]

    for client in data['clients']:
        path = search_for_substation(client, adj_list, powerlines)
        for line in path:
            line['beforecolor'] += 1

    for facility in output.keys():
        if 'dummy' in facility:
            for client in output[facility]:
                path = search_for_substation(facility, adj_list, powerlines)
                for line in path:
                    line['aftercolor'] += 1
        else:
            path = search_for_substation(facility, adj_list, powerlines)
            for line in path:
                line['aftercolor'] += 1

    for line in powerlines:
        line['aftercolor'] = num_to_color(line['aftercolor'], line['capacity'])
        line['beforecolor'] = num_to_color(line['beforecolor'], line['capacity'])

