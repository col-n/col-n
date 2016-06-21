#challenge 4

import binascii
import col_n_chal_3

def mylines(fname):
	f = open(fname, 'r')
	for line in f:
		if line[-1] == '\n':
			line = line[:-1]
		s = binascii.unhexlify(line)
		return s

def findthexor(lines):
	bustedlines = [col_n_chal_3.bustxor(1)[1] for l in lines]
	def score(i):
		return col_n_chal_3.score(bustedlines[i])
	maxi = max(range(len(bustedlines)), key = score)
	return (maxi+1, bustedlines[maxi])

print(findthexor(mylines('4.txt')))