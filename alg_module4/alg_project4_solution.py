"""
alg project 4

Computing alignments of sequences

2014, Oct 12th
"""

# Modelling matrices
# we will model these matrices as lists of lists in Python and can 
# access a particular entry vid 'alignment_matrix[row][col]'

# Also we will represent a scoring matrix in Python as a dictionary
# of dictionaries


# Matrix functions
def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
	"""
	build a scoring matrix as a dictionary of dictionaries
	alphabet is a set of characters
	e.g. M['A']['C'] is the score that we get when aligning 'A' and 'C'.
	"""
	alphabet_list = list(alphabet)
	scoring_matrix = {alpha:{} for alpha in alphabet_list}
	for col in scoring_matrix:
		for row in alphabet_list:
			if col=='-' or row=='-':
				scoring_matrix[col][row] = dash_score
			elif col == row:
				scoring_matrix[col][row] = diag_score
			else:
				scoring_matrix[col][row] = off_diag_score


	return scoring_matrix


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
	"""
	computes either a global alignment matrix or a local alignment matrix
	depending on the value of global_flag
	return the dynamic programming table S (lists of lists)
	e.g. S[2][2] is the maximal score that we can get when aligning the 
	first two letters of the first sequence with the first two letters of 
	the second sequence 
	"""
	alignment_matrix = [[0 for jdx in range(len(seq_y)+1)] \
		for idx in range(len(seq_x)+1)]

	for idx in range(1,len(seq_x)+1):
		if global_flag:
			alignment_matrix[idx][0] = alignment_matrix[idx-1][0] + scoring_matrix[seq_x[idx-1]]['-']
		else:
			# local alignment matrix
			alignment_matrix[idx][0] = max(0, alignment_matrix[idx-1][0] + scoring_matrix[seq_x[idx-1]]['-'])

	for jdx in range(1,len(seq_y)+1):
		if global_flag:
			alignment_matrix[0][jdx] = alignment_matrix[0][jdx-1] + scoring_matrix['-'][seq_y[jdx-1]]
		else:
			# local alignment matrix
			alignment_matrix[0][jdx] = max(0, alignment_matrix[0][jdx-1] + scoring_matrix['-'][seq_y[jdx-1]])

	for idx in range(1,len(seq_x)+1):
		for jdx in range(1,len(seq_y)+1):
			if global_flag:
				alignment_matrix[idx][jdx] = max(
					alignment_matrix[idx-1][jdx-1] + scoring_matrix[seq_x[idx-1]][seq_y[jdx-1]],
					alignment_matrix[idx-1][jdx] + scoring_matrix[seq_x[idx-1]]['-'],
					alignment_matrix[idx][jdx-1] + scoring_matrix['-'][seq_y[jdx-1]])
			else:
				# local alignment matrix
				alignment_matrix[idx][jdx] = max( 0,
					alignment_matrix[idx-1][jdx-1] + scoring_matrix[seq_x[idx-1]][seq_y[jdx-1]],
					alignment_matrix[idx-1][jdx] + scoring_matrix[seq_x[idx-1]]['-'],
					alignment_matrix[idx][jdx-1] + scoring_matrix['-'][seq_y[jdx-1]])
	return alignment_matrix


# Alignment functions
def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
	"""
	the function return a tuple of the form (score, align_x, align_y) where
	score is the score of the global alignment align_x and align_y.
	"""
	idx_x = len(seq_x)
	idx_y = len(seq_y)
	align_x, align_y = '', ''
	while idx_x!=0 and idx_y!=0:
		if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x-1][idx_y-1] + scoring_matrix[seq_x[idx_x-1]][seq_y[idx_y-1]]:
			align_x = seq_x[idx_x-1] + align_x
			align_y = seq_y[idx_y-1] + align_y
			idx_x -= 1
			idx_y -= 1
		elif alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x-1][idx_y] + scoring_matrix[seq_x[idx_x-1]]['-']:
			align_x = seq_x[idx_x-1] + align_x
			align_y = '-'+align_y
			idx_x -= 1
		else:
			align_x = '-'+align_x
			align_y = seq_y[idx_y-1] + align_y
			idx_y -= 1
	
	while idx_x!=0:
		align_x = seq_x[idx_x-1] + align_x
		align_y = '-'+align_y
		idx_x -= 1
	
	while idx_y!=0:
		align_x = '-'+align_x
		align_y = seq_y[idx_y-1] + align_y
		idx_y -= 1			
	
	score = compute_alignment_matrix(align_x, align_y, scoring_matrix, global_flag=True)[-1][-1]	
	return (score, align_x, align_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
	"""
	the function return a tuple of the form (score, align_x, align_y) where
	score is the score of the local alignment align_x and align_y.
	Start the traceback from the entry in S that has the maximum value over
	the entire matrix and trace backward using exactly the same technique 
	as in compute_global_alignment.
	Stop the traceback when the first entry with value 0 is encoutered.	
	"""
	# Start the traceback from the entry in S that has the maximum value over
	# the entire matrix	
	max_score = 0
	# print alignment_matrix
	idx_x, idx_y = len(seq_x), len(seq_y)
	for row in range(len(alignment_matrix)):
		for col in range(len(alignment_matrix[row])):
			if alignment_matrix[row][col]> max_score:
				max_score = alignment_matrix[row][col]
				idx_x, idx_y = row, col
				# print "idx_x,idx_y",idx_x, idx_y
	align_x, align_y = '', ''
	while idx_x!=0 and idx_y!=0:
		if alignment_matrix[idx_x][idx_y] == 0:
			break
		if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x-1][idx_y-1] + scoring_matrix[seq_x[idx_x-1]][seq_y[idx_y-1]]:
			align_x = seq_x[idx_x-1] + align_x
			align_y = seq_y[idx_y-1] + align_y
			idx_x -= 1
			idx_y -= 1
		elif alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x-1][idx_y] + scoring_matrix[seq_x[idx_x-1]]['-']:
			align_x = seq_x[idx_x-1] + align_x
			align_y = '-'+align_y
			idx_x -= 1
		else:
			align_x = '-'+align_x
			align_y = seq_y[idx_y-1] + align_y
			idx_y -= 1
	
	while idx_x!=0:
		if alignment_matrix[idx_x][idx_y] == 0:
			break
		align_x = seq_x[idx_x-1] + align_x
		align_y = '-'+align_y
		idx_x -= 1
	
	while idx_y!=0:
		if alignment_matrix[idx_x][idx_y] == 0:
			break		
		align_x = '-'+align_x
		align_y = seq_y[idx_y-1] + align_y
		idx_y -= 1			
	
	score = compute_alignment_matrix(align_x, align_y, scoring_matrix, global_flag=False)[-1][-1]	
	return (score, align_x, align_y)




