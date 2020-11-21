import json
import itertools
import copy
import argparse
from argparse import RawTextHelpFormatter


def check_mogaraba(bayt):
	"""
	Five mota7areek is not allowed 
	"""
	b = "".join(bayt.split())
	f = "".join(["o" if b[i] == 'ْ' else "|" for i in range(1,len(b),2)])
	return "|||||" not in f,f

class Z7afElal:
	def __init__(self,name, operation):
		self._name = name
		self._operation = operation
	def apply(self,taf3eela):
		return self._operation[taf3eela]

class Ba7ar:
	def __init__(self,name,base,rules):
		self._name = name
		self._base = base
		self._rules = rules
		self._parts = self._base.split()
	def get_permutations(self,btype):
		rules = self._rules[btype]
		perms_taf = []
		perms_misht = []
		# looping over rules set for @btybe (e.g. tam, majzoo2)
		for ruleset in rules:
			# getting all permutation for a single ruleset
			perms = [' '.join(str(y) for y in x) for x in itertools.product(*ruleset.values())]
			# looping over z7af and 3elal permutations
			for p in perms:
				# apply single permutation ze7af and 3elal
				p = p.split()
				idxs = [int(i) for i in list(ruleset.keys())]
				taf = []
				for ze,tidx in zip(p,idxs):
					taf.append(Z7AFELAL[ze].apply(self._parts[tidx]))

				#  check if misht (kitaba aroodiya e.g |o|||o) is already existing and no mogaraba (five |||||)
				## This might be slow but sufficient for problem scale
				taf = " ".join(taf)
				good,misht = check_mogaraba(taf)
				if good and misht not in perms_misht:
					perms_taf.append(taf)
					perms_misht.append(misht)
		return perms_taf


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Bo7oor Alshe3r',formatter_class=RawTextHelpFormatter)
	parser.add_argument('--ba7ar_name',help='wafir\nhazj\nkamil\nrajz\nraml\nmotagarib\ntaweel\nmotadarak\nbasse6\nmadid\nsaree3\nmonsare7\nmogtadeb\nmojtath\nkhafeef\nmodare3\n')
	parser.add_argument('--ba7ar_type',help='tam\nmajzoo2\nmash6oor\nmanhook\nmo5alla3\nmowa77ad')
	parser.add_argument('--count_all', action='store_true')
	args = parser.parse_args()
	
	# reading data
	with open("./data.json") as f:
		data = json.load(f)

	# loading all z7af and 3elal
	Z7AFELAL = {}
	for ze in data["Z7afElal"]:
		Z7AFELAL[ze["name"]] = Z7afElal(**ze)

	# loading b7oors
	B7OOR = {}
	for b7r in data["Bo77or"]:
		B7OOR[b7r["name"]] = Ba7ar(**b7r)

	# if count all 
	if args.count_all:
		count = 0
		for bk,b7r in B7OOR.items():
			for rule in b7r._rules:
				perms =  b7r.get_permutations(rule)
				count += len(perms)
		print(count)
	# print permutations of a certain ba7ar (e.g. taweel) with a certain type (e.g. tam, majzoo2)
	else:
		for perm in B7OOR[args.ba7ar_name].get_permutations(args.ba7ar_type):
			print(perm)


