import music
import collections
from nose.tools import assert_equals

class Graph():
  """Basic adjacency-list graph."""
  def __init__(self, n):
    self.s = Node.Marker("S")
    self.t = Node.Marker("T")
    self.n = n
    self.edges = collections.defaultdict(list)
    self.nodes = [[] for i in range(n+2)]
    self.nodes[0].append(self.s)
    self.nodes[-1].append(self.t)

  def _add_node(self, node, layer):
    # If called from add_nodes, ensures that all nodes in the preceding layer
    # will have edges to this node.
    assert layer > 0 and layer <= self.n
    self.nodes[layer].append(node)
    for v in self.nodes[layer-1]:
      self.edges[v].append((node, v.dist(node)))

  def add_nodes(self, nodes):
    """Builds a DAG where each node in layer i has an edge to all nodes in layer i+1.
    Nodes is a list of lists of nodes. Partitioned by layer.
    Will also insert a starting node, self.s, and an ending node, self.t
    """
    for layer in range(1, len(nodes)+1):
      for node in nodes[layer-1]:
        self._add_node(node, layer)
    for node in nodes[-1]:
      self.edges[node].append((self.t, node.dist(self.t)))

  def dfs(self):
    """Yields s-t paths."""
    stack = [(self.s, [])]
    while stack:
      curr, parents = stack.pop()
      if curr == self.t:
        yield parents
        continue
      for node, dist in self.edges[curr]:
        if curr != self.s:
          stack.append((node, parents + [curr]))
        else:
          stack.append((node, parents))

  @property
  def num_edges(self):
    # Only used for testing
    return sum((len(v) for v in self.edges.values()))

class Node():
  """Represents one way of playing a particular chord with a particular fingering."""
  def __init__(self, chord, fingers):
    assert len(fingers) == 4
    self.chord = chord
    self.fingers = fingers

  def dist(self, other):
    """Proportional to the difficulty of moving your hand from self.fingering to other.fingering."""
    total = 0
    for i in range(len(self.fingers)):
      if None in (self.fingers[i], other.fingers[i]) or 0 in (self.fingers[i], other.fingers[i]):
        continue
      else:
        total += abs(self.fingers[i] - other.fingers[i])
    return total

  def __str__(self):
    assert len(self.fingers) == 4
    s = ""
    for i in self.fingers:
      if i is None: 
        s += "."
      else:
        s += ",%s" % i
    return self.chord + ": " + s[1:]

  @staticmethod
  def Marker(symbol):
    """Yields special nodes that don't correspond to fingerings."""
    return Node(symbol, [None, None, None, None])

def progressions(chords, n=10):
  """Yields pairs of (score, fingering_list). Each fingering list produces the given chord progression. Sorted by difficulty, ascending."""
  g = Graph(len(chords))
  nodes = []
  for chord in chords:
    chord_nodes = []
    for fingering, notes in music.fingers_for_chord(chord):
      chord_nodes.append(Node(chord, fingering))
    nodes.append(chord_nodes)
  g.add_nodes(nodes)
  min_paths = sorted([(path_dist(path), path) for path in g.dfs()])
  for score, path in min_paths[:n]:
    yield score, "\t".join(map(str, path))

def path_dist(path):
  """Total distance between all fingerings in a path."""
  total = 0
  for u, v in (path[:-1], path[1:]):
    total += u.dist(v)
  return total


def test_dist():
  a = Node("A", [None, 1, 1, 1])
  b = Node("B", [2, 2, 2, None])
  c = Node("C", [2, 2, 3, None])
  d = Node("D", [4, 1, 2, 3])
  e = Node("E", [14, 11, 12, 13])
  assert_equals(0, a.dist(a))
  assert_equals(0, b.dist(b))
  assert_equals(2, a.dist(b))
  assert_equals(2, b.dist(a))
  assert_equals(1, b.dist(c))
  assert_equals(1, c.dist(b))
  assert_equals(40, e.dist(d))
  assert_equals(40, d.dist(e))

def test_graph_small():
  g = Graph(2)
  assert_equals(0, g.num_edges)
  a = Node("A", [1, 1, 1, 1])
  b = Node("A", [2, 2, 2, 2])
  c = Node("B", [3, 3, 3, 3])
  d = Node("B", [4, 4, 4, 4])
  g.add_nodes([[a,b], [c,d]])
  assert_equals(8, g.num_edges)
  assert_equals(2, len(g.edges[g.s]))
  assert_equals(2, len(g.edges[a]))
  assert_equals(2, len(g.edges[b]))
  assert_equals([(g.t, 0)], g.edges[c])
  assert_equals([(g.t, 0)], g.edges[d])

def test_dfs():
  g = Graph(2)
  assert_equals(0, g.num_edges)
  g.add_nodes([
    [Node("A", [1, 1, 1, 1]), Node("A", [2, 2, 2, 2])],
    [Node("B", [3, 3, 3, 3]), Node("B", [4, 4, 4, 4])],
    ])
  assert_equals(8, g.num_edges)
  paths = {tuple(path) for path in g.dfs()}
  for path in paths:
    assert_equals(["A", "B"], [node.chord for node in path])
  assert_equals(4, len(paths))


if __name__ == "__main__":
  for x in progressions(["F", "G", "A"]):
    print x




