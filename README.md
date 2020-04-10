# Insight Data Engineering - Coding Challenge - Consumer Complaints

## Table of Contents
1. [Problem](README.md#problem)
2. [Input Dataset](README.md#input-dataset)
3. [Assumptions](README.md#assumptions)
4. [How to run](README.md#how-to-run)
5. [Approach](README.md#approach)
6. [The output](README.md#the-output)
7. [Instructions](README.md#instructions)
8. [Handling nuances](README.md#handling-nuances)
9. [Where it won't work](README.md#where-it-won't-work)

## Problem
The federal government provides a way for consumers to file complaints against companies regarding different financial products, such as payment problems with a credit card or debt collection tactics. This challenge is about identifying the number of complaints filed and how they're spread across different companies. 

**For this challenge, we want to know for each financial product and year, the total number of complaints, number of companies receiving a complaint, and the highest percentage of complaints directed at a single company. The output needs to be sorted in alphabetical order for `Product` and ascending order for `year`.

## Input dataset

Below are the contents of an example `complaints.csv` file: 
```
Date received,Product,Sub-product,Issue,Sub-issue,Consumer complaint narrative,Company public response,Company,State,ZIP code,Tags,Consumer consent provided?,Submitted via,Date sent to company,Company response to consumer,Timely response?,Consumer disputed?,Complaint ID
2019-09-24,Debt collection,I do not know,Attempts to collect debt not owed,Debt is not yours,"transworld systems inc. is trying to collect a debt that is not mine, not owed and is inaccurate.",,TRANSWORLD SYSTEMS INC,FL,335XX,,Consent provided,Web,2019-09-24,Closed with explanation,Yes,N/A,3384392
2019-09-19,"Credit reporting, credit repair services, or other personal consumer reports",Credit reporting,Incorrect information on your report,Information belongs to someone else,,Company has responded to the consumer and the CFPB and chooses not to provide a public response,Experian Information Solutions Inc.,PA,15206,,Consent not provided,Web,2019-09-20,Closed with non-monetary relief,Yes,N/A,3379500
2020-01-06,"Credit reporting, credit repair services, or other personal consumer reports",Credit reporting,Incorrect information on your report,Information belongs to someone else,,,Experian Information Solutions Inc.,CA,92532,,N/A,Email,2020-01-06,In progress,Yes,N/A,3486776
2019-10-24,"Credit reporting, credit repair services, or other personal consumer reports",Credit reporting,Incorrect information on your report,Information belongs to someone else,,Company has responded to the consumer and the CFPB and chooses not to provide a public response,"TRANSUNION INTERMEDIATE HOLDINGS, INC.",CA,925XX,,Other,Web,2019-10-24,Closed with explanation,Yes,N/A,3416481
2019-11-20,"Credit reporting, credit repair services, or other personal consumer reports",Credit reporting,Incorrect information on your report,Account information incorrect,I would like the credit bureau to correct my XXXX XXXX XXXX XXXX balance. My correct balance is XXXX,Company has responded to the consumer and the CFPB and chooses not to provide a public response,"TRANSUNION INTERMEDIATE HOLDINGS, INC.",TX,77004,,Consent provided,Web,2019-11-20,Closed with explanation,Yes,N/A,3444592
```
Each line of the input file, except for the first-line header, represents one complaint. Consult the [Consumer Finance Protection Bureau's technical documentation](https://cfpb.github.io/api/ccdb/fields.html) for a description of each field.  


## Assumptions

Following are some of the assumptions my code makes in order to perform this task:
* The input file is in the same format as the sample input described in the section [Input Dataset](README.md#input-dataset). This means that my code expects each input file to have a header. It also expects each column to be in the same order as the sample input above.
* The date is of the form "YYYY-MM-DD". In general, this code will work for any input where the first 4 characters of the column `Date received` represent the year.
* All the `Product` and `Company` names are case insesitive. For example, "Acme", "ACME", and "acme" would represent the same company.
* The column `Product` is a categorical variable and only takes in values described as per the [Consumer Finance Protection Bureau's technical documentation](https://cfpb.github.io/api/ccdb/fields.html). This wouldn't neccessarily be a problem though. See section [Where it won't work](README.md#where-it-won't-work) to see cases where this code might fail. 

## How to run

The main `Python` script is present in `./src`. It can be run by using the following command `python3.7 ./src/generate_report.py <input_file_path> <output_file_path>`. For our case, the exact command would be:
```
python3.7 ./src/generate_report.py ./input/complaints.csv ./output/report.csv
```
We can also use the Shell script, `run.sh` to run the code.

## Approach

The key idea behind my approach is the fact that there are a lot of redundant columns in our data that we don't need and that all we need is the number of complaints at a `Product-Year-Company` level in order to get all the information needed to prepare the output. This can very easily be done by using `Dictionaries`. I use the `defaultdict` structure simply because it eliminates the need to check whether a key is already present in the dictionary. While this does not offer a direct improvement in the performance of the code, it certainly leads to better readability. 

The input is read line by line and thus can read any amount of data. We only store the necessary information namely `Product`, `Year`, `Company` and the number of complaints for each combination of these and discard the remaining information. This is done by storing this info in a dictionary called `all_complaints` with its key being a concatenated form of `Product`, `Year` and `Company` and the value being the number of complaints.

We simultaneously update another dictionary called `complaints_summary` which as the name suggests stores the summary of the complaint database. This summary is maintained at a `Product` and `Year` level. This is done by using `Product` as the key for the dictionary and its value being another dictionary. The inner dictionary has `Year` as the key and it contains a list of 3 numbers. For a given value of `Product` and `Year`, these numbers represent the following in the same order:
* Maximum number of complaints registered for a single company for that particular combination of `Product` and `Year` - This is calculated by looking at the value of num of complaints in the `all_complaints` dictionary for any combination and storing its max value at all times in the corresponding `Product-Year` combination in `complaints_summary`
* Total number of complaints made for that particular combination of `Product` and `Year` - This is calculated by summing all complaints for the corresponding `Product-Year` combination in `all_complaints` regardless of the company
* Number of companies for which at least onbe complaint was made for that particular combination of `Product` and `Year`- This is calculated by looking at the number of companies for which the corresponding `Product-Year-Company` combination would have exactly 1 complaints at any time in `all_complaints`. Note that this would happen exactly once for each company.

For the sample input given above, this is how `complaints_summary` would look like:
```
complaints_summary = {
                     debt collection: {2019: [1,1,1]},
                     credit reporting, credit repair services, or other personal consumer reports: {2019: [2,3,2], 2020: [1,1,1]}
                     }
```

Finally the keys of this dictionary are sorted and we loop over it to write the output in the desired format. Please note that since all the information is already present in the dictionary `complaints_summary`, which was prepared while reading the data itself, there is no need for any additional processing.

## The output

After reading and processing the input file, this code will create an output file, `report.csv`, with as many lines as unique pairs of product and year (of `Date received`) in the input file. 

Each line in the output file will list the following fields in the following order:
* product (name should be written in all lowercase)
* year
* total number of complaints received for that product and year
* total number of companies receiving at least one complaint for that product and year
* highest percentage (rounded to the nearest whole number) of total complaints filed against one company for that product and year. Use standard rounding conventions (i.e., Any percentage between 0.5% and 1%, inclusive, should round to 1% and anything less than 0.5% should round to 0%)

The lines in the output file will be sorted by product (alphabetically) and year (ascending)

Given the above sample input file, we'd expect an output file, `report.csv`, in the following format
```
"credit reporting, credit repair services, or other personal consumer reports",2019,3,2,67
"credit reporting, credit repair services, or other personal consumer reports",2020,1,1,100
debt collection,2019,1,1,100
```
Notice that because `debt collection` was only listed for 2019 and not 2020, the output file only has a single entry for debt collection. Also, notice that when a product has a comma (`,`) in the name, the name is enclosed by double quotation marks (`"`). Finally, notice that percentages are listed as numbers and do not have `%` in them.

## Handling nuances

## Where it won't work

