"""
processDNAta.py
version 9/5/2014

Author: Ellen Blaine

This program takes in a folder containing files of exon sequences and returns 
data about those files in the form of a CSV file, including which species 
for whom a sequence was recovered, the percentage AT/CG bias, and the median 
recovered sequence length. This program is meant to be used in conjunction 
with TEF and AlignHelper.

Important Note: The input files' sequences should contain question marks to
indicate a sequence was NOT recovered. Questionable nucleotides should be identified
as N's or another character, but NOT question marks. If '?' is found at the 
beginning of a sequence, the program will assume that sequence was NOT recovered.

Sample input: python processDNAta_v1.py AlignHelper_Output SpeciesNames.txt
"""
from sys import argv
import os

script, folder, species = argv

path = folder + '/'
listing = os.listdir(path)
newfile = open("processDNAta_Output.csv", 'w')

def createdict(infile):
	file_path = path 
	file = open(file_path, 'r')
	dict = {}
	seq = ""
	name = ""
	for line in file:
		if line.startswith('>'):
			dict[name] = seq
			name = line
			seq = ""
		else:
			seq += line
	for line in file:
		seq += line
	dict[name] = seq
	return dict
		
def searchdict(item, dict):
	for key in dict.keys():
		if item.rstrip() in key and not dict.get(key).startswith('?'):
			return True
	return False
	
def findbias(dict):	
	ATcount = 0
	CGcount = 0
	ATCGcount = 0
	for value in dict.values():
		if not value.startswith('?'):
			for index in range(0,len(value)):
				if value[index] == 'A' or value[index] == 'T':
					ATcount += 1
					ATCGcount += 1
				if value[index] == 'C' or value[index] == 'G':
					CGcount += 1
					ATCGcount += 1
	percentAT = float(ATcount)/ATCGcount * 100
	percentCG = float(CGcount)/ATCGcount * 100
	return percentAT, percentCG

species_list = []
species_file = open(species, 'r')
newfile.write(" ,")
for line in species_file:
	species_list.append(line.rstrip())
	newfile.write(line.rstrip() + ", ")
newfile.write("% AT bias, % CG bias, ")
newfile.write("Median Sequence Length (bp)")
newfile.write('\n')

def findmedian(dict):
	dict.pop(">" + infile[:infile.find('.')] + "\n")
	lengths = []
	for value in dict.values():
		if not value.startswith('?'):
			lengths.append(len(value))
	lengths.sort()
	middle_index = len(lengths)/2
	if len(lengths) % 2 == 1:
		return lengths[middle_index]
	else:
		median = (lengths[middle_index] + lengths[middle_index - 1]) / 2
		return median

for infile in listing:
	if ".fasta" in infile:
		path = folder + '/' + infile
		dict = createdict(infile)
		file = open(path, 'r')
		newfile.write(infile[:infile.find('.')] + ", ")
		for item in species_list:
			if searchdict(item, dict):
				newfile.write("1, ")
			else:
				newfile.write("0, ")
		percentAT, percentCG = findbias(dict)
		median = findmedian(dict)
		newfile.write(str(percentAT) + "%, " + str(percentCG) + "%, ")
		newfile.write(str(median) + "\n")
		
			
