"""
algorithmic thinking

Project2
Connected components and graph resilience

yusong shen

2014.09.13

"""

# use python built-in queue data structure
from collections import deque
import random

# the graph is represented as a dictionary
GRAPH1 = {0:set([1, 2, 3, 4, 5]),
		  1: set([0, 2, 3, 4, 5]),
          2: set([0, 1, 3, 4, 5]),
          3: set([0, 1, 2, 4, 5]),
          4: set([0, 1, 2, 3, 5]),
          5: set([0, 1, 2, 3, 4]),
          6: set([])}

# Breadth-first search
def bfs_visited(ugraph, start_node):
	"""
	takes the undirected graph ugraph and the node start_node
	and return the set consiting of all nodes that are visited by a 
	Breadth-first search that starts at start_node
	"""
	queue = deque()
	visited = [start_node]
	queue.append(start_node)
	# print queue
	while len(queue)!=0:		
		current_node = queue.pop()
		neighbours = list(ugraph[current_node])
		# print neighbours
		for neighbour in neighbours:
			if neighbour not in visited:
				visited.append(neighbour)
				queue.append(neighbour)
	return set(visited) 



# connected components
def cc_visited(ugraph):
	"""
	takes the undirected graph ugraph and returns a list of sets,
	where each set consists of all the nodes (and nothing else) in 
	a connected component, and there is exactly one set in the
	list for each connected component in ugraph and nothing else
	"""
	remaining_nodes = ugraph.keys()
	connected_components = [] 
	while len(remaining_nodes)!=0:
		node = random.choice(remaining_nodes)
		visited = bfs_visited(ugraph, node)
		connected_components.append(visited)
		for visited_node in visited:
			remaining_nodes.remove(visited_node)
	return connected_components

def largest_cc_size(ugraph):
	"""
	takes the undirected graph ugraph and return the size of the 
	largest connected component in ugraph
	"""
	max_size = 0
	connected_components = cc_visited(ugraph)
	for component in connected_components:
		if len(component)>max_size:
			max_size = len(component)
	return max_size

# Graph resilience
def compute_resilience(ugraph, attack_order):
	"""
	takes the undirected graph ugraph, a list of nodes attack_order
	and iterates through the nodes in attack_order. For each node 
	in the list, the function removes the given node and its edges
	from the graph and then computes the size of the largest connected
	component for the resulting graph.
	"""
	resilience = []
	# first entry is the size of the largest connected component
	# in the original graph
	resilience.append(largest_cc_size(ugraph))
	for node in attack_order:
		# remove the node and its edges in ugraph
		# Todo
		for neighbour in ugraph[node]:
			ugraph[neighbour].remove(node)
		del ugraph[node]
		resilience.append(largest_cc_size(ugraph))
	return resilience


# test suit
def test():
	"""
	test all the three functions
	"""
	# expected = set([node for node in range(6)])
	# result = bfs_visited(GRAPH1, 1)
	# if expected == result:
	# 	print "true"
	# 	print "expected:",expected
	# else:
	# 	print "false"
	# 	print "expected:",expected
	# 	print "result:",result

	# expected = [set([0,1,2,3,4,5]),set([6])]	
	# result = cc_visited(GRAPH1)

	# expected = 6	
	# result = largest_cc_size(GRAPH1)

	expected = [6, 5, 4, 3]
	attack_order = [1, 2, 3]	
	result = compute_resilience(GRAPH1, attack_order)	
	if expected == result:
		print "true"
		print "expected:",expected
	else:
		print "false"
		print "expected:",expected
		print "result:",result

# test()