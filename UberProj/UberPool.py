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
''''

gr = Graph()
mode  = 0
for line in fileinput.input():
    comp = line.split(" ")
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
            dist, path = dijsktra(gr, node1)
            print(dist[node2])
        else:
            dist, path = dijsktra(gr, node2)


