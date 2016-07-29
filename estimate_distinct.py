import hashlib
import random
import numpy as np
from collections import Counter

HASH_BIT_NUM = 128

MAX_LONG = 2**HASH_BIT_NUM - 1


def min_hashes_by_hash_func(items , k):
	"""

	Parameters:
	----------
	items : arraylike
		collecton of strings

	k : int
		number of hash functions to be used on each item

	Returns:
	-------
	min_hashes: arraylike
		minimum across all items for each of the k hash functions
	"""

	def normalize_hash(hashed_item):
		"""
		Map a 128-bit long hash to the unit interval

		Parameters:
		----------
		hash_item : long
			128-bit hash

		Returns:
		-------
		norm_hash : float
			hash in [0, 1]
		"""
		return hashed_item / float(MAX_LONG)

	random_bit_strings = [random.getrandbits(HASH_BIT_NUM) for i in xrange(k-1)]

	all_hashes = np.zeros((len(items), k))

	for i in xrange(len(items)):
		item_hash = int(hashlib.md5(items[i]).hexdigest(), 16)
		all_hashes[i, 0] =  normalize_hash(item_hash)
		
		for j in xrange(len(random_bit_strings)):
			all_hashes[i, j+1] = normalize_hash(item_hash ^ random_bit_strings[j])

	return np.amin(all_hashes, 0)


def num_items_from_min_dist(min_dist):
	"""
	Returns, form the minimum value of a hash callection, an estimate of the number
	of items in that collection

	Parameters:
	----------
	min_dist : float
		minimum distance in a collection of hashes on the unit interval

	Returns:
	-------
	estimate : float
		estimate of the number of elements in the collection holding min_dist
	
	"""
	return (1 / min_dist) - 1

def estimateDistinctElements(items, k):
	"""
	Use the idea of min-hash signatures to estimate the number of unique elements in a sequence

	1. Hash each of the elements in the sequence on the interval [0, 1]
	2. Take the min of those hashes
	3. This min (e) is expectd 1 / (N + 1) => N = (1 / e) - 1


	Parameters:
	----------

	items : sequence of elements
	k:  number of hash functions

	RETURNS:
	-------
	estimate : estimate of the number of distinct elements in the sequence
	"""
	if len(items) == 0:
		return 0

	min_hashes = min_hashes_by_hash_func(items, k)

	e = min_hashes.mean()

	return num_items_from_min_dist(e)


def estimateDistinctElementsParallel(listsOfItems, k):
	"""
	Estimate cardinality of a set via distributabled operations 
	(i.e. independent and identical calculations on separate portions of a set) 

	Params:
	------
	listsOfItems : arraylike of arraylike
		wish to estimate the cardinality of the union of the collections within this collection
	k : int
		number of hash functions

	Returns:
	-------
	estimate : float
		estimate of the number of distinct elements in total sequence
	"""
	if len(listsOfItems) == 0:
		return 0

	sequence_min_hashes = map(lambda seq: min_hashes_by_hash_func(seq, k), listsOfItems)

	all_hashes = np.vstack(sequence_min_hashes)

	e = np.amin(all_hashes, 0).mean()

	return num_items_from_min_dist(e)


def calculateEmpiricalAccuracy(items, estimate):
	"""
	Calculate estimate - actual. Note returned value can be positive or negative

	Params:
	------
	items: arraylike or arraylike of arraylike
		the sequence or list of sequences under consideration
	estimate:
		guess of the cardinality of the set

	Returns:
	-------
	difference : float
		difference between estimated size and actual size of underlying set.
	"""
	if len(items) == 0:
		return estimate

	if type(items[0]) == list:
		return estimate - len(reduce(lambda x, y: x | y, map(set, items)))
	return estimate - len(set(items))