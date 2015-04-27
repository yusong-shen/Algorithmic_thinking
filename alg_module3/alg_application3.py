"""
algorithmic thinking 

module 3 application
comparison of clustering algorithms

author : yusong shen
2014.09.28

 In this Application, we will analyze the performance of these two
 methods on various subsets of our county-level cancer risk data set.
 In particular, we will compare these two clustering methods 
 in three areas:

Efficiency - Which method computes clusterings more efficiently?
Automation - Which method requires less human supervision
			 to generate reasonable clusterings?
Quality - Which method generates clusterings with less error?

"""

from alg_project3_solution import *
import timeit
import random
import alg_cluster
import matplotlib.pyplot as plt
import time


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])]
            for tokens in data_tokens]


# Efficiency : Q1-Q4
# Question 1
def gen_random_clusters(num_clusters):
	"""
	create a list of clusters where each cluster in this list corresponds 
	to one randomly generated point in the square with corners
	(+-1,+-1)
	"""
	clusters = [alg_cluster.Cluster(set(), random.uniform(-1, 1), random.uniform(-1, 1), 0, 0)
	            for idx in range(num_clusters)]
	return clusters


def run_example_q1():
	"""
	compute the running times of the functions slow_closest_pairs and fast_closest_pair
	for lists of random clusters of size 2 to 200
	plot thhe result as two curves combined in a single plot
	"""
	sizes = range(2, 201)
	time_list1 = []
	time_list2 = []
	for size in sizes:
		random_clusters = gen_random_clusters(size)
		start = time.clock()
		slow_closest_pairs(random_clusters)
		finish = time.clock()
		time1 = finish - start

		start = time.clock()
		fast_closest_pair(random_clusters)
		finish = time.clock()
		time2 = finish - start
		# timer1 = timeit.Timer("alg_project3_solution.slow_closest_pairs(alg_project3_solution.random_clusters)",
		# "import alg_project3_solution")
		# time1 = min(timer1.repeat(3,1))
		# timer2 = timeit.Timer("alg_project3_solution.fast_closest_pair(alg_project3_solution.random_clusters)",
		# "import alg_project3_solution")
		# time2 = min(timer1.repeat(3,1))
		time_list1.append(time1)
		time_list2.append(time2)
	# print "time1",time1
	# print "time2",time2
	# print

	# plot
	plt.figure(1)
	plt.plot(sizes, time_list1, label="slow_closest_pairs")
	plt.plot(sizes, time_list2, label="fast_closest_pair")
	plt.legend()
	plt.xlabel('the input size of random clusters')
	plt.ylabel('the running time of two clustreing methods (seconds)')
	plt.grid(True)
	plt.title("comparison of efficiency for slow_closest_pairs and fast_closest_pair")

	plt.show()


# Automation : Q5-Q9
# Question 7
def compute_distortion(cluster_list, data_table):
	"""
	take a list of clusters and uses method cluster_error in Cluster class
	to compute its distortion .
	"""
	distortion = 0.0
	for cluster in cluster_list:
		error = cluster.cluster_error(data_table)
		distortion += error
	return distortion


# Quality : Q10-12
# def compare_distortion(singleton_list_h,singleton_list_k , data_table):
# 	"""
# 	compare the distortion produce by hierarchical and k-means clustering
# 	use the number of cluster range from 6 to 20
# 	plot the distortion with the input number of cluster
# 	"""
# 	len_data = len(data_table)
# 	sizes = range(6, 21)
# 	distortions_hier = []
# 	distortions_kmeans = []
# 	for size in sizes:
# 		cluster_list_h = hierarchical_clustering(singleton_list_h, size)
# 		cluster_list_k = kmeans_clustering(singleton_list_k, size, 5)
# 		distortions_hier.append( compute_distortion(cluster_list_h, data_table) )
# 		distortions_kmeans.append( compute_distortion(cluster_list_k, data_table) )
# 	print "distortions_hier", distortions_hier
# 	print "distortions_kmeans", distortions_kmeans
# 	# plot
# 	plt.figure(1)
# 	plt.plot(sizes, distortions_hier, label="hierarchical clustering")
# 	plt.plot(sizes, distortions_kmeans, label="k-means clustering")
# 	plt.legend()
# 	plt.xlabel('the input size of clusters')
# 	plt.ylabel('the distortion of two clustreing methods')
# 	plt.grid(True)
# 	plt.title("comparison of distortion for hierarchical and k-means clustering, %d county data sets"%(len_data))
#
# 	plt.show()


def compare_distortion(data_table):
	"""
	compare the distortion produce by hierarchical and k-means clustering
	use the number of cluster range from 6 to 20
	plot the distortion with the input number of cluster
	"""
	len_data = len(data_table)
	sizes = range(6, 21)
	distortions_hier = []
	distortions_kmeans = []
	for size in sizes:
		singleton_list_h = []
		singleton_list_k = []
		for line in data_table:
		    singleton_list_h.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
			# make a copy
		    singleton_list_k.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

		# this line make a refernce ?
		# singleton_list_k = singleton_list_h

		cluster_list_h = hierarchical_clustering(singleton_list_h, size)
		cluster_list_k = kmeans_clustering(singleton_list_k, size, 5)
		distortions_hier.append( compute_distortion(cluster_list_h, data_table) )
		distortions_kmeans.append( compute_distortion(cluster_list_k, data_table) )
	print "distortions_hier", distortions_hier
	print "distortions_kmeans", distortions_kmeans


	# plot
	plt.figure(1)
	plt.plot(sizes, distortions_hier, label="hierarchical clustering")
	plt.plot(sizes, distortions_kmeans, label="k-means clustering")
	plt.legend()
	plt.xlabel('the input size of clusters')
	plt.ylabel('the distortion of two clustreing methods')
	plt.grid(True)
	plt.title("comparison of distortion for hierarchical and k-means clustering, %d county data sets"%(len_data))

	plt.show()

# Testing

# print gen_random_clusters(10)
# run_example_q1()



	