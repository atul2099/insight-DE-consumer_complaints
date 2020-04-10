#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""generate_report.py

"""

import csv
import sys
from collections import defaultdict

def get_data(filename):
	with open(filename, "r") as f:
		file_reader = csv.reader(f)
		header = next(file_reader)
		for line in file_reader:
			features = [line[0][:4],line[1].lower(),line[7].lower()]
			yield features

def write_data(filename,complaints_summary,min_year,max_year):
	with open(filename, "w", newline='') as f:
		file_writer = csv.writer(f)
		for product in sorted(complaints_summary):
			for year in range(min_year,max_year+1):
				max_complaints, total_complaints, num_companies = complaints_summary[product][str(year)]

				if total_complaints > 0:
					row = [product,year,total_complaints,num_companies,round(max_complaints*100/total_complaints)]
					file_writer.writerow(row)

def main(input_path,output_path):
	file_reader = get_data(input_path)

	all_complaints = defaultdict(int)
	complaints_summary = defaultdict(lambda: defaultdict(lambda: [0,0,0]))

	min_year = 9999
	max_year = -1

	for line in file_reader:
		year, product, company = line
		if int(year) < min_year:
			min_year = int(year)
	    
		if int(year) > max_year:
			max_year = int(year)
	    
		all_complaints[product+year+company] += 1
	    
		max_complaints, total_complaints, num_companies = complaints_summary[product][year]
	    
		total_complaints += 1
	    
		if all_complaints[product+year+company] > max_complaints:
			max_complaints = all_complaints[product+year+company]
	        
		if all_complaints[product+year+company] == 1:
			num_companies += 1
	        
		complaints_summary[product][year] = [max_complaints, total_complaints, num_companies]

	write_data(output_path,complaints_summary,min_year,max_year)

if __name__ == '__main__':

	# Assign input and output files.
	input_file_path = sys.argv[1]
	output_file_path = sys.argv[2]

	main(input_file_path,output_file_path)