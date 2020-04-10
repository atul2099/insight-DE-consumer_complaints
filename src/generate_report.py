#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""generate_report.py

"""

# Library imports
import csv
import sys
from collections import defaultdict

# Utility functions
def get_data(filename):
	with open(filename, "r", encoding="utf8") as f:
		file_reader = csv.reader(f)

		# Disregarding the first line of the file (header)
		header = next(file_reader)

		# Reading the input line by line and only returning the important information
		for line in file_reader:
			year = line[0][:4]
			product = line[1].lower()
			company = line[7].lower()
			row = [year,product,company]
			yield row

def write_data(filename,complaints_summary,min_year,max_year):
	with open(filename, "w", newline='') as f:
		file_writer = csv.writer(f)

		# Loop over sorted keys of complaint_summary
		for product in sorted(complaints_summary):

			# Instead of sorting the year evertime, loop over all possible values of year
			for year in range(min_year,max_year+1):
				max_complaints, total_complaints, num_companies = complaints_summary[product][str(year)]

				# Only write to disk if there is at least one complaint for a product in a year
				if total_complaints > 0:
					row = [product,year,total_complaints,num_companies,round(max_complaints*100/total_complaints)]
					file_writer.writerow(row)

def main(input_path,output_path):
	# Get the generator for reading input
	file_reader = get_data(input_path)

	# Initialize variables
	all_complaints = defaultdict(int)
	complaints_summary = defaultdict(lambda: defaultdict(lambda: [0,0,0]))
	min_year = 9999
	max_year = -1

	for line in file_reader:
		year, product, company = line

		# Update min and max values of the year (used later to skip sorting)
		if int(year) < min_year:
			min_year = int(year)
	    
		if int(year) > max_year:
			max_year = int(year)
	    
	    # Each row in our input refers to one complaint
		all_complaints[product+year+company] += 1
	    
	    # Read current values
		max_complaints, total_complaints, num_companies = complaints_summary[product][year]
	    
	    # Each row in our input refers to one complaint
		total_complaints += 1

		# Update the max complaints to any company for a given product and year	    
		if all_complaints[product+year+company] > max_complaints:
			max_complaints = all_complaints[product+year+company]
	        
		# This happens only once for each company for a given combination of Product and year
		if all_complaints[product+year+company] == 1:
			num_companies += 1
	        
	    # Update new values
		complaints_summary[product][year] = [max_complaints, total_complaints, num_companies]

	# Finally write everything to disk
	write_data(output_path,complaints_summary,min_year,max_year)

if __name__ == '__main__':

	# Assign input and output files.
	input_file_path = sys.argv[1]
	output_file_path = sys.argv[2]

	main(input_file_path,output_file_path)