"""
module 4 test


"""

from alg_project4_solution import *

alphabet = set(['A','C','T','G','-'])

def test():
	"""
	test suit for module 4
	"""
	scoring_matrix = build_scoring_matrix(alphabet, diag_score=5, 
		off_diag_score=2, dash_score=-6)
	print scoring_matrix

	seq_x = 'AC'
	seq_y = 'TA'
	alignment_matrix = compute_alignment_matrix(seq_x, seq_y, 
		scoring_matrix, global_flag=True)
	print alignment_matrix

	result = compute_global_alignment('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 
	 	'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 
	 	'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0]]) 
	expected =  (0, '', '')
	print "result:",result
	print "expected:",expected 
	assert result==expected,'compute_global_alignment go wrong'

	result = compute_local_alignment('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 
		'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 
		'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0]])
	expected =  (0, '', '')
	print "result:",result
	print "expected:",expected 
	assert result==expected,'compute_local_alignment go wrong'

test()

