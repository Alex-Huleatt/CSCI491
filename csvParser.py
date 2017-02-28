
import sys
from array import array

verbose = True

line_chunk_size = 2**10

test_rows = [0, 1, 2] + range(1020, 1030)

class CSV():

	def __init__(self, fname):
		self.fname = fname
		self.f = open(fname)
		self.chunks = []
		self._offset = 0
		self.id_list = []
		self._test_rows = []

	def __del__(self):
		self.f.close() #make sure to close file on destruction of object.

	#returns the file offest of each (2**10)th line.
	#so the first element is the position of 1024th row
	#run this only once.
	def get_chunks(self, i, line): 
		if i % line_chunk_size == 0:
			self.chunks.append(self.f.tell())
		

	#binary search
	def findID(self, toFind):
		lo, hi = 0, len(self.id_list)
		mid = (lo+hi)//2
		idx = -1
		while lo < hi:
			v = self.id_list[mid][1]
			if v > toFind:
				hi = mid-1
			elif v < toFind:
				lo = mid+1
			else:
				idx = self.id_list[mid][0]
				break
			mid = (hi+lo)//2
		return idx
	
	#using our chunks, query for some line.
	#makes querying rows O(1), instead of O(n) in the size of the csv.
	def get_row(self, n):
		n-=1
		chunk = n//line_chunk_size
		self.f.seek(self.chunks[chunk])
		for k in range(n%line_chunk_size):
			self.f.readline() #keep scanning
		return self.f.readline()

	def get_row_bad(self, n):
		self.f.seek(0,0)
		for i in range(n+1):
			self.f.readline()
		return self.f.readline()
		
	def populate_ids(self, i, line):
		if i in test_rows:
			self._test_rows.append((line))
		d = line[1:line.find(',')-1] #this will be the id number
		self.id_list.append((i, int(d))) #associate an id with the row it occurs in.
	
	#passes over the full file, each function in before_list will be called with a (i, line), where i is the index of the line
	#after iterating over the whole file, each function in after list will be called.
	def full_pass(self, before_list, after_list):
		if verbose:
			print 'Doing full pass over:', self.fname
			print 'Calling:', str([k.__name__ for k in before_list])
		i = 0
		line = self.f.readline()
		while line:	
			if i != 0:
				for c in before_list:
					c(self, i-1,line)
			line = self.f.readline()
			i+=1
		if verbose:
			print self.fname+':','Full pass over file complete.'
			print 'Calling:', str([k.__name__ for k in after_list])
		for a in after_list:
			a(self)

	def sort_ids(self):
		if verbose:
			print 'Sorting ids for', self.fname
		self.id_list.sort(key=lambda x:x[1])
		if verbose:
			print 'Sorted ids for', self.fname


full = CSV(sys.argv[1])
full.full_pass([CSV.get_chunks, CSV.populate_ids], [CSV.sort_ids])
# for i in range(len(test_rows)):
# 	r = full.get_row(test_rows[i])
# 	r2 = full.get_row_bad(test_rows[i])
# 	print test_rows[i], 'get_row:', r[0:r.find(',')], 'Actual:', r2[0:r2.find(',')]
up = CSV(sys.argv[2])
up.full_pass([CSV.get_chunks, CSV.populate_ids], [])
no_find = []
found = 0
for k in up.id_list:
	index = full.findID(k[1])
	if index != -1:
		r = full.get_row(index)
		found+=1
	else:
		no_find.append(k[1])

print "Couldn't find:", no_find
print 'Found %s out of %s' % (found, len(up.id_list))

