import numpy as np
from estimate_distinct import estimateDistinctElements, estimateDistinctElementsParallel

def get_sample(size):
	"""
	Helper function to get a sample of random numbers

	Params:
	------
	size : int 
		size of desired sample

	Returns:
	-------
	sample : arraylike
	"""
	return map(str, np.random.randint(0, 2000000, size=size))


def print_test_report(estimated, actual, test_no):
	print "TEST #%d" % test_no
	print "Estimated cardinality: %.2f" % estimated
	print "Actual cardinality: %d" % actual
	print "Error %%: %.2f" % (abs(actual - estimated) * 100 / actual)
	print "\n--------------------\n"


def get_actual_cardinality(set_structure):
	"""
	Params:
	------
	set_structure : arraylike or arraylike or arraylike
	"""
	if len(set_structure) == 0:
		return 0

	if type(set_structure[0]) == list:
		return len(reduce(lambda x, y: x | y, map(set, set_structure)))
	return len(set(set_structure))



def test1():
	sample = get_sample(1000)
	print_test_report(estimateDistinctElements(sample, 1000), get_actual_cardinality(sample), 1)

def test2():
	listOfSamples = [get_sample(100) for i in xrange(1000)]
	print_test_report(estimateDistinctElementsParallel(listOfSamples, 1000), get_actual_cardinality(listOfSamples), 2)

test1()
test2()