"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster
import random
# import operator

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), idx1, idx2)


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    # Brute force method
    # return a set of pairs that share the minimal distance and 
    # the returned indices should be ordered
    # idx1 < idx2
    closest_pairs = [(float('Inf'), -1, -1)]
    for idx1 in range(len(cluster_list)):
        for idx2 in range(len(cluster_list)):
            if idx1 < idx2:
                dist = pair_distance(cluster_list, idx1, idx2)[0]
                min_dist = closest_pairs[0][0]
                # print "dist", dist
                # print "min_dist", min_dist
                if dist < min_dist:
                    closest_pairs = [(dist, idx1, idx2)]
                elif dist == min_dist:
                    closest_pairs.append((dist, idx1, idx2))             
    return set(closest_pairs)


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
    
    # ensure that implementations of lines9-10,14 in the pseudo-code are O(n)
    # hint: the lists Hl and Hr can be temporarily converted to sets    
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        # use some helper functions to reduce local variable and branch...
        def copy_points_helper(horiz_order, vert_order, len_h):
            """
             copy the point indices to avoid repeating computation
            """
            horiz_left = [horiz_order[idx] for idx in range(len_h/2)]
            horiz_left_set = set([horiz_order[idx] for idx in range(len_h/2)])
            # the bug that took me two hours = =!
            horiz_right =[horiz_order[idx] for idx in range(len_h/2,len_h)]
            horiz_right_set = set([horiz_order[idx] for idx in range(len_h/2,len_h)])
            # change the list horiz_left to set
            # the search tiem reduce from O(n) to O(1)
            vert_left = [cluster for cluster in vert_order
                         if cluster in horiz_left_set ]
            vert_right = [cluster for cluster in vert_order
                          if cluster in horiz_right_set]
            return horiz_left, horiz_right, vert_left, vert_right

        def cluster_mid_helper(horiz_order, vert_order, len_h):
            """
            copy the point indices that fall in the middle
            len_h means the length of the cluster list
            """
            horiz_cood_l = cluster_list[horiz_order[len_h/2-1]].horiz_center()
            horiz_cood_r = cluster_list[horiz_order[len_h/2]].horiz_center()
            mid = 0.5*(horiz_cood_l+horiz_cood_r)
            clusters_mid = [ idx for idx in vert_order
                             if abs(cluster_list[idx].horiz_center() - mid) < closest_pair[0] ]
            return clusters_mid


        len_h = len(horiz_order)
        # base case
        if len_h <= 3:
            small_cluster_list = [cluster_list[horiz_order[idx]] for idx in range(len(horiz_order))]
            # this indice range from 0 to 2, which is not the real indice
            # use the horiz_order list to get the real indices
            temp_closest_pair = list(slow_closest_pairs(small_cluster_list))[0]
            return (temp_closest_pair[0], horiz_order[temp_closest_pair[1]], horiz_order[temp_closest_pair[2]])
        # divide
        else:
            # copy the point indices to avoid repeating computation
            horiz_left, horiz_right, vert_left, vert_right = copy_points_helper(horiz_order, vert_order, len_h)
            # find the closest pair in each half
            closest_pair_l = fast_helper(cluster_list, horiz_left, vert_left)
            closest_pair_r = fast_helper(cluster_list, horiz_right, vert_right)
            closest_pair = min(closest_pair_l, closest_pair_r)

        # conquer
            # copy the point indices that fall in the middle
            clusters_mid = cluster_mid_helper(horiz_order, vert_order, len_h)
            # compute the distance of pairs in the middle
            # compare them to the closest pair in half
            # we can only compare the three nearest neighbour points(in y coordinate) for each point
            for idx1 in range(len(clusters_mid)-1):
                for idx2 in range(idx1+1,min(idx1+3,len(clusters_mid)-1)+1):
                    # note!! Here index should use the real index
                    dist_mid = pair_distance(cluster_list, clusters_mid[idx1], clusters_mid[idx2])[0]
                    closest_pair = min(closest_pair, (dist_mid, clusters_mid[idx1], clusters_mid[idx2]))
        return closest_pair
            
    # compute list of indices for the clusters ordered in the horizontal direction
    # H
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    # V
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))

    

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    # initialize n cluster
    cluster_result = cluster_list
    while len(cluster_result) > num_clusters:
        closest_pair = fast_closest_pair(cluster_result)
        # closest_pair = list(slow_closest_pairs(cluster_result))[0]
        # merge the closest pairs by using merge_clusters() method
        # then remove the original clusters
        cluster_result[closest_pair[1]].merge_clusters(cluster_result[closest_pair[2]])
        # del cluster_result[closest_pair[2]]
        # make some optimization
        # swich the original cluster to the end of the list ,then use pop() method
        # reduce the time from O(n) to O(1)
        cluster_result[closest_pair[2]],cluster_result[-1] = cluster_result[-1], cluster_result[closest_pair[2]]
        cluster_result.pop()
    return cluster_result



    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    # sort the cluster_list according to the population
    cluster_list = sorted(cluster_list,key = lambda cluster : cluster.total_population(), reverse=True)
    # initialize k-means clusters to be initial clusters with largest populations
    # maintain two lists : the old one update once in every outer iteration
    #                      the new one update in every point
    k_clusters_old = cluster_list[:num_clusters]
    k_centers = [(cluster.horiz_center(),cluster.vert_center()) for cluster in k_clusters_old]
    for idx in range(num_iterations):
        # the cluster centers should stay fixed when merge happen
        # so I store them in a separate list

        # initialize new clusters: k empty sets in each iteration
        # they will be filled with the clusters assigned to the corresponding centers
        # and with zero population and no fips codes
        k_clusters = [alg_cluster.Cluster(set(),center[0], center[1], 0, 0) for center in k_centers ]
        for idx1 in range(len(cluster_list)):
            # '+ idx ' is nonsense= =
            # for each point , find the closest cluster it belongs to
            min_distance = float("inf")
            # make sure use the center of cluster stored before
            # because the center of current cluster change all the time during merging
            distances = [cluster_list[idx1].distance(cluster) for cluster in k_clusters_old]
            # enumerate function generate (index, value)
            closest_cluster_idx,closest_cluster = min(enumerate(distances), key = lambda p: p[1])
            # merge this point to that cluster
            # and the merge function also recompute the center for each cluster
            # this line mutate the new clusters- k_clusters
            k_clusters[closest_cluster_idx].merge_clusters(cluster_list[idx1])
        # the old clusters update every outer iteration
        k_clusters_old = k_clusters
        # # '+ idx ' is nonsense= =
        # num_iterations += idx - idx
    return k_clusters




