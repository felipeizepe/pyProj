import fileinput
import collections

class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = collections.defaultdict(list)
    self.distances = {}

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):
    self.edges[from_node].append(to_node)
    #self.edges[to_node].append(from_node)
    self.distances[(from_node, to_node)] = distance


def dijsktra(graph, initial):
  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes:
    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
        break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited, path


def inconv(gr,a,b,c):
  dist1, path1 = dijsktra(gr, a)
  dist2, path2 = dijsktra(gr, b)

  inconvAC = dist1[c]
  inconvAB = dist1[b]
  inconvBC = dist2[c]

  inconvTotal = (inconvAB + inconvBC) / inconvAC
  return inconvTotal


def inconv2(gr, a, b, c, d):
    dist1, path1 = dijsktra(gr, a)
    dist2, path2 = dijsktra(gr, d)
    dist3, path2 = dijsktra(gr, c)

    inconvAB = dist1[b]
    inconvAC = dist1[c]
    inconvCD = dist3[d]
    inconvDB = dist2[b]

    inconvTotal = (inconvAC + inconvCD + inconvDB) / inconvAB
    return inconvTotal

def getTrip(gr, tripA, tripB, isRunning):
    pass1 = tripA[0][0]
    pass2 = tripB[0][0]

    nodeA = tripA[1][0]
    nodeB = tripA[1][1]

    nodeC = tripB[1][0]
    nodeD = tripB[1][1]


    incA1 = inconv(gr, nodeA, nodeC, nodeB)
    incA1_2 = inconv(gr, nodeC, nodeB, nodeD)
    incA2 = inconv2(gr, nodeA, nodeB, nodeC, nodeD)
    incB1 = inconv(gr, nodeC, nodeA, nodeD)
    incB1_2 = inconv(gr, nodeA, nodeD, nodeB)
    incB2 = inconv2(gr, nodeC, nodeD, nodeA, nodeB)

    if isRunning:
        if incA1 < 1.4 and incA1_2 < 1.4 and incA1 <= incA2:
            return [[[pass1, pass2], [nodeA, nodeC, nodeB, nodeD], True]]
        elif incA2 < 1.4:
            return [[[pass1, pass2], [nodeA, nodeC, nodeD, nodeB], True]]
        else:
            list = []
            list.append([[pass1], [nodeA, nodeB], isRunning])
            list.append([[pass2], [nodeC, nodeD], False])
            return list

    if incA1 < 1.4 and incA1_2 < 1.4 and incA1 <= incA2 and incA1 <= incB1 and incA1 <= incB2:
        return [[[pass1, pass2], [nodeA, nodeC, nodeB, nodeD], True]]
    elif incA2 < 1.4 and incA2 <= incB1 and incA2 <= incB2:
        return [[[pass1, pass2], [nodeA, nodeC, nodeD, nodeB], True]]
    elif incB1 < 1.4 and incB1_2 < 1.4 and incB1 <= incB2:
        return [[[pass1, pass2], [nodeC, nodeA, nodeD, nodeB], True]]
    elif incB2 < 1.4:
        return [[[pass1, pass2], [nodeC, nodeA, nodeB, nodeD], True]]
    else:
        list = []
        list.append([[pass1], [nodeA, nodeB], isRunning])
        list.append([[pass2], [nodeC, nodeD], False])
        return list

def findTrips(gr, trips):
    newTrips = trips
    i = 0
    j = 0
    while i < len(trips) - 1:
        while j < len(trips):
            if i == j:
                j += 1
            else:
                tripA = newTrips[i]
                tripB = newTrips[j]

                if len(tripA[0]) > 1:
                    j += 1
                elif tripB[2]:
                    j += 1
                else:
                    calc_trip = getTrip(gr, tripA, tripB, tripA[2])
                    print calc_trip
                    del newTrips[j]
                    del newTrips[i]
                    newTrips.extend(calc_trip)
                    if j == len(trips) - 1:
                        j += 1
        j = 0
        i += 1

    return newTrips

''''
#example inconv usage
grEx = Graph()

#A
grEx.add_node(0)
#B
grEx.add_node(1)
#C
grEx.add_node(2)

#AC
grEx.add_edge(0, 2, 2)
#AB
grEx.add_edge(0, 1, 2)
#BC
grEx.add_edge(1, 2, 2)

print(inconv(grEx,0,1,2))
'''

gr = Graph()
mode  = 0
count = 1
trips = []
for line in fileinput.input():
    comp = line.split(" ")

    if comp[0] == '':
        del comp[0]

    if line == "\n":
        mode += 1
        continue

    node1 = int(comp[0])
    node2 = int(comp[1])

    if mode == 0:
        edge = float(comp[2])
        gr.add_node(node1)
        gr.add_node(node2)
        gr.add_edge(node1, node2, edge)
    elif mode == 1:
        if len(comp) < 3:
            node = []
            passa = []
            paths = []
            passa.append(count)
            paths.append(node1)
            paths.append(node2)
            node.append(passa)
            node.append(paths)
            node.append(False)
            trips.append(node)
            count += 1
        else:
            node3 = int(comp[2])
            node = []
            passa = []
            paths = []
            passa.append(count)
            paths.append(node3)
            paths.append(node2)
            node.append(passa)
            node.append(paths)
            node.append(True)
            trips.append(node)
            count += 1

results = findTrips(gr, trips)

for result in results:

    perc = ""
    for per in result[1]:
        perc = perc + str(per) + " "

    if len(result[0]) > 1:
        pass1 = result[0][0]
        pass2 = result[0][1]

        out = "passageiros " + str(pass1) + " e " + str(pass2) + " percurso: " + perc
        print out
    else:
        pass1 = result[0][0]

        out = "passageiro " + str(pass1) + " percurso: " + perc
        print out
