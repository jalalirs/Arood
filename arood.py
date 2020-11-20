import json
import itertools
import copy
import argparse
from argparse import RawTextHelpFormatter

BAD = 0

def check_mogaraba(bayt):
	b = "".join(bayt.split())
	f = ["o" if b[i] == 'ْ' else "|" for i in range(1,len(b),2)]
	count = 0
	for c in f:
		if c == "|":
			count += 1
			if count == 5:
				return False
		else:
			count = 0
	return True

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
		global BAD
		rules = self._rules[btype]
		perms_taf = []
		for ruleset in rules:
			perms = [' '.join(str(y) for y in x) for x in itertools.product(*ruleset.values())]
			for p in perms:
				p = p.split()
				taf = []
				idxs = [int(i) for i in list(ruleset.keys())]
				for ze,tidx in zip(p,idxs):
					taf.append(Z7AFELAL[ze].apply(self._parts[tidx]))
				taf = " ".join(taf)
				if check_mogaraba(taf):
					perms_taf.append(taf)
				else:
					print(taf)
					BAD += 1
		return perms_taf


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Bo7oor Alshe3r',formatter_class=RawTextHelpFormatter)
	parser.add_argument('--ba7ar_name', required=True,help='wafir\nhazj\nkamil\nrajz\nraml\nmotagarib\ntaweel\nmotadarak\nbasse6\nmadid\nsaree3\nmonsare7\nmogtadeb\nmojtath\nkhafeef\nmodare3\n')
	parser.add_argument('--ba7ar_type', required=True,help='tam\nmajzoo2\nmash6oor\nmanhook\nmo5alla3\nmowa77ad')
	args = parser.parse_args()
	
	with open("./data.json") as f:
		data = json.load(f)

	Z7AFELAL = {}
	for ze in data["Z7afElal"]:
		Z7AFELAL[ze["name"]] = Z7afElal(**ze)


	B7OOR = {}
	for b7r in data["Bo77or"]:
		B7OOR[b7r["name"]] = Ba7ar(**b7r)


	for perm in B7OOR[args.ba7ar_name].get_permutations(args.ba7ar_type):
		print(perm)
	count = 0
	for bk,b7r in B7OOR.items():
		for rule in b7r._rules:
			perms =  b7r.get_permutations(rule)
			count += len(perms)
	print(count,BAD)
