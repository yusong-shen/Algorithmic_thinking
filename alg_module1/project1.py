"""
Project 1 

Degree distributions for graphs

Algorithmic Thinking
"""

import alg_module1_graphs

# representing directed graphs as dictionary
EX_GRAPH0 = {0:set([1,2]),
			 1:set([]),
			 2:set([]) } 

EX_GRAPH1 = {0:set([1, 4, 5]),
		  1: set([2, 6]),
          2: set([3]),
          3: set([0]),
          4: set([1]),
          5: set([2]),
          6: set([])}

EX_GRAPH2 = {0:set([1, 4, 5]),
		  1: set([2, 6]),
          2: set([3, 7]),
          3: set([7]),
          4: set([1]),
          5: set([2]),
          6: set([]),
          7: set([3]),
          8: set([1, 2]),
          9: set([0, 3, 4, 5, 6, 7])}


def make_complete_graph(num_nodes):
	""" 
	return a dictionary corresponding to a completed directed
	graph with the specified number of num_nodes, like
	GRAPH0 = {0: set([1,2,3]),
          1: set([0,2,3]),
          2: set([0,1,3]),
          3: set([0,1,3])}
	"""
	digraph = {}
	for node in range(num_nodes):
		neighbours = []
		for neighbour in range(num_nodes):
			if neighbour != node:
				neighbours.append(neighbour)
		digraph[node]=set(neighbours)
	return digraph
	

# computing degree distributions
def compute_in_degrees(digraph):
	"""
	take a directed graph represented as a dictionary and 
	compute the in-degrees for the nodes in the graph,
	return a dictionary like {a:2,b:2,c:2}
	"""
	in_degrees = {}
	for node in digraph:
		in_degree = 0
		for neighbour in digraph:
			if node != neighbour:
				if node in digraph[neighbour]:
					in_degree += 1 
		in_degrees[node] = in_degree

	return in_degrees

def in_degree_distribution(digraph):
	"""
	return a dictionary whose keys corresponding to in-degrees 
	of nodes in the graph, and the value associate with each 
	particular node is the the number of nodes with that in-degrees,
	like {2:3}
	"""
	distribution = {}
	in_degrees = compute_in_degrees(digraph)
	for node in in_degrees:
		in_degree = in_degrees[node]
		if in_degree not in distribution:
			distribution[in_degree] = 1
		else:
			distribution[in_degree] += 1

	return distribution

# digraph1 = make_complete_graph(6)
# print digraph1
# print alg_module1_graphs.GRAPH0
# digraph1 = alg_module1_graphs.GRAPH0
# in_degrees = compute_in_degrees(digraph1)
# print in_degrees

# distribution = in_degree_distribution(digraph1)
# print distribution

