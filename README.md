# MyBhutan

To successfully launch the Excel model, please make sure:
- all the files (analysis.py, book1 and your csv file) are in the same directory
- the input has to be a csv file with the same format as payments.csv
- you have python 3.6 installed on your laptop

Output sheet "Result" is in "Book1.xls", we named:
- "floating fee" the fee expressed as a percent
- "fix cost" the constant part of the fee


How to use this model?
	1) Make sure your input file has the same format as the csv payments.csv (if not, ask the Columbia Team to make the modification in the code). Put this csv in the same directory as the excel file
	2) Click on the button below
	3) Browse your csv file
	4) A new sheet has been created with your results
	5) Two tables are displayed: the first one uses the first model (flat model) and gives you the costs associated with the flat fee per month with all the transaction you gave in input; the second table uses the second model to calculate the IC costs (according to your revenue, either option 1,2 or 3 is chosen)
Note: if you want to choose the IC fee chosen to compute model 2, it has to be directly modified in the python file. Do not hesitate to ask the Columbia team.

All the calculations are computed in the file "analysis.py", interchange rate and all the fees can easily be changed in the model inside this file.

