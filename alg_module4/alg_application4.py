"""
Provide code and solution for Application 4

alg application 4
Applications to genomics and beyond

Author:Yusong Shen

2014, Oct 14th

"""

DESKTOP = True

import math
import random
import urllib2
import time

if DESKTOP:
    import matplotlib.pyplot as plt
    from alg_project4_solution import *
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"

# Local file
PAM50 = "alg_PAM50.txt"
HUMAN_EYELESS = "alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS = "alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX = "alg_ConsensusPAXDomain.txt"
WORD_LIST = "assets_scrabble_words3.txt"


###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    # scoring_file = urllib2.urlopen(filename)
    scoring_file = open(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    # protein_file = urllib2.urlopen(filename)
    protein_file = open(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    # word_file = urllib2.urlopen(filename)
    word_file = open(filename)

    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


# #----------------------------------------------------------------------
# Comparing two proteins
# Q1
# First,load the files using the provided code
pam50_scoring_dict = read_scoring_matrix(PAM50)
human_protein_seq = read_protein(HUMAN_EYELESS)
fruitfly_protein_seq = read_protein(FRUITFLY_EYELESS)

# print "pam50_scoring_dict",pam50_scoring_dict
print len(human_protein_seq),len(fruitfly_protein_seq)
print "human_protein_seq:",human_protein_seq[:10]
print "fruitfly_protein_seq",fruitfly_protein_seq[:10]

# Next,compute the local alignment of the sequence of human_protein_seq
# and fruitfly_protein_seq using pam50_scoring_dict
alignment_matrix = compute_alignment_matrix(human_protein_seq, fruitfly_protein_seq, 
        pam50_scoring_dict, global_flag=False)
(score_normal, align_hum, align_fru) = compute_local_alignment(human_protein_seq, fruitfly_protein_seq, 
    pam50_scoring_dict, alignment_matrix)

print "score:",score_normal
print "align_hum:",align_hum
print "align_fru:",align_fru


# Q2
# Load the file CONSENSUS_PAX
consensus_seq = read_protein(CONSENSUS_PAX)
# print "consensus_seq:"consensus_seq
# print len(consensus_seq)


def compare_similarity(local_align_seq, consensus_seq):
    """
    return two percentages: one for each global alignment
    """
    # delete any dashes in the two local sequence in Q1
    for char in local_align_seq:
        if char == '-':
            local_align_seq = local_align_seq.replace(char,'')
    # print "local_align_seq without dash:",local_align_seq
    assert '-' not in local_align_seq,"local_align_seq still has dash!"

    # compute the global alignment
    alignment_matrix = compute_alignment_matrix(local_align_seq, consensus_seq,
        pam50_scoring_dict, global_flag=True)
    (score, align_x, align_y) = compute_global_alignment(local_align_seq, consensus_seq, 
        pam50_scoring_dict, alignment_matrix) 
    # print "score:",score
    # print "align_x:",align_x
    # print "align_y:",align_y  
    # print "len(align_x)=",len(align_x) 
    # compare local vs. consensus
    same_char = 0.0
    for idx in range(len(align_x)):
        if align_x[idx]==align_y[idx]:
            same_char += 1

    return same_char/len(align_x)

per_hum_con = compare_similarity(align_hum, consensus_seq)
per_fru_con = compare_similarity(align_fru, consensus_seq)
print "per_hum_con:",per_hum_con
print "per_fru_con:",per_fru_con



# Hypothesis testing
# Q4
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    return a dictonary scoring_distribution that represents an 
    unnormalized distribution generated by performing the following 
    process num_trials times.
    """
    scoring_distribution = {}
    # generate a random permutation rand_y of the sequence seq_y
    # using random.shuffle()
    seq_y_list = list(seq_y)
    for idx in range(num_trials):        
        # print seq_y_list
        random.shuffle(seq_y_list)
        rand_y = ''.join(seq_y_list)
        # compute the maximum value score for the local alignment of 
        # seq_x and rand_y
        alignment_matrix = compute_alignment_matrix(seq_x, rand_y,
            scoring_matrix, global_flag=False)
        score = alignment_matrix[-1][-1]
        # Increment the entry score in the dictionary scoring_distribution
        # by 1
        if score in scoring_distribution:
            scoring_distribution[score] += 1
        else:
            scoring_distribution[score] = 1

    return scoring_distribution

start = time.clock()
num_trials = 1000
# # non-normalized distribution
# scoring_distribution = generate_null_distribution(human_protein_seq,
#     fruitfly_protein_seq, pam50_scoring_dict, num_trials)

# print "scoring_distribution:",scoring_distribution
finish = time.clock()
print "using %f second to run"%(finish-start)


# create a bar plot of the normalized version of the scoring_distribution
# for score in scoring_distribution:
#     scoring_distribution[score] /=float(num_trials)

# print scoring_distribution
def plot_distribution(scoring_distribution):
    """
    input the non-normalize distribution
    plot the scoring_distribution
    """
    for score in scoring_distribution:
        scoring_distribution[score] /=float(num_trials)    
    scores = scoring_distribution.keys()
    # print "scores:",scores
    prob = [scoring_distribution[score] for score in scores]
    plt.figure(1)
    plt.bar(scores, prob)
    plt.ylabel("probability of each score")
    plt.xlabel("score for the local alignment of human_protein_seq and random fruitfly_protein_seq")
    plt.title("scoring_distribution for the local alignment of human_protein_seq and random fruitfly_protein_seq")

    plt.show()



# Q6
def statistical_analysis(scoring_distribution, num_trials):
    """
    return mean, standard_deviation
    """
    mean = 0.0
    standard_deviation = 0.0
    for score in scoring_distribution:
        mean += score*scoring_distribution[score]*num_trials
    mean /= num_trials
    for score in scoring_distribution:
        standard_deviation += scoring_distribution[score]*num_trials*(score - mean)**2
    standard_deviation = (standard_deviation/num_trials)**0.5
    return mean, standard_deviation

# Normalized distribution
scoring_distribution = {38: 0.001, 39: 0.001, 40: 0.005, 41: 0.015, 42: 0.025, 43: 0.033, 44: 0.035, 
    45: 0.061, 46: 0.053, 47: 0.067, 48: 0.066, 49: 0.07, 50: 0.053, 51: 0.066, 
    52: 0.051, 53: 0.063, 54: 0.045, 55: 0.039, 56: 0.041, 57: 0.025, 58: 0.036, 59: 0.031,
    60: 0.014, 61: 0.015, 62: 0.017, 63: 0.009, 64: 0.009, 65: 0.012, 66: 0.004, 
    67: 0.005, 68: 0.004, 69: 0.002, 70: 0.008, 71: 0.004, 72: 0.004, 73: 0.001, 
    74:0.001, 75: 0.002, 76: 0.002, 78: 0.001, 79: 0.002, 80: 0.001, 87: 0.001}


mean, standard_deviation = statistical_analysis(scoring_distribution, num_trials)
z_score = (score_normal - mean)/standard_deviation

print "mean:",mean
print "standard_deviation:",standard_deviation
print "z_score",z_score


# #------------------
# Spelling Correction
# Q8
alphabet = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','-'])
edit_dist_scores = build_scoring_matrix(alphabet, diag_score=2, off_diag_score=1, dash_score=0)

def check_spelling(checked_word, dist, word_list):
    """
    iterates through word_list and returns the set of all words that
    are within edit distance dist of the string checked_word
    """
    result = []
    for word in word_list:
        alignment_matrix = compute_alignment_matrix(word, checked_word,
            edit_dist_scores, global_flag=True)
        score_xy = alignment_matrix[-1][-1]
        edit_dist = len(word) + len(checked_word) - score_xy
        if edit_dist <= dist:
            result.append(word)
    return set(result)


# load the list of 79430 words
word_list = read_words(WORD_LIST)
checked_word = "humble"
dist = 1
result_words = check_spelling(checked_word, dist, word_list)
print result_words
checked_word = "firefly"
dist = 2
result_words = check_spelling(checked_word, dist, word_list)
print result_words

# Q9
# design a spelling Correction tool that would provide real-time
# correction of spelling errors within edit distance of two

# hint
# 1. covert the list of provided words to a set of words
# 2 focus on the structure of the three editing operations :
# insert , delete, substitute
