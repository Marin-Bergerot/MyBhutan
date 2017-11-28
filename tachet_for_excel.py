import sys
import csv
import os
import time
from math import *



if len(sys.argv) != 5 and len(sys.argv) != 1:
		sys.exit("usage: analyze.py datafilename outputfilename namein nameout\n")

elif len(sys.argv)==1:
	try:
		output = open('hidden.txt', 'w') # opens the file
		
	except IOError:
		print("Cannot open outputfile file hidden.txt for writing\n")

elif len(sys.argv)==5:

	def get_month(date):
		letter=date[0]
		a=date[1]
		if a!="/":
			return letter+a
		else:
			return letter
			
	def get_year(date):
		compt=0
		nb_sign=0
		while nb_sign!=2:
			if date[compt]=="/":
				nb_sign+=1
			compt+=1
		year=""
		
		while date[compt]!=" ":
			year+=date[compt]
			compt+=1
		if len(year)==2:
			return "20"+year
		return year
		
	def ic_estimator(date):
		#Should use l[row][3], the amount; l[row][10], the brand of the card ans l[row][11], the type of the card.
		#I do not know to what refers l[row][4], fees and l[row][5], taxes, but they may be included?
		#For now, I return a classical IC for a Visa Credit Card
		#First element is percentage, second is fixed cost
		return [0.02,.1]
		
	def model1(payments,sums,alpha_large,alpha_small,fix_cost):
		#model if we do not take care of the IC, using stripe's first offer
		list_of_costs={}
		for i in payments.keys():
			list_of_costs[i]=[]
			if sums[i]>=80000:
				alpha=alpha_small
			else:
				alpha=alpha_large
			list_of_costs[i].append(alpha)
			total_cost=0
			for j in payments[i]:
				total_cost+=alpha*j+fix_cost
			list_of_costs[i].append(total_cost)
		return list_of_costs

	def model2(payments,sums,alpha_large,alha_medium,alpha_small,fix_cost_large,fix_cost_medium,fix_cost_small):
		#model taking care of the IC, ie stripe's second offer
		list_of_costs={}
		for i in payments.keys():
			list_of_costs[i]=[]
			IC=ic_estimator(i)
			if sums[i]<1000000:
				print("You got under the limit scale to benefit from our plan, bye bye")
				return 0
			elif sums[i]<=3000000:
				alpha=alpha_large
				fix_cost=fix_cost_large
			elif sums[i]<=6000000:
				alpha=alpha_medium
				fix_cost=fix_cost_medium
			else:
				alpha=alpha_small
				fix_cost=fix_cost_small
			list_of_costs[i].append(IC)
			list_of_costs[i].append(alpha)
			list_of_costs[i].append(fix_cost)
			total_cost=0
			for j in payments[i]:
				total_cost+=(IC[0]+alpha)*j+fix_cost+IC[1]
			list_of_costs[i].append(total_cost)
		return list_of_costs

	departure=time.time()

	



	#now reading and copying the data from the input file
	l=[]
	try: 
		datafile= open(sys.argv[1], 'r') 
		reader = csv.reader(datafile)
		for row in reader:
			l.append(row)
		datafile.close
	except IOError:
		sys.exit("Cannot open file %s\n" % sys.argv[1])

	#now opening the output file to write
	try:
		output = open(sys.argv[2], 'w') # opens the file
	except IOError:
		print("Cannot open outputfile file %s for writing\n" % sys.argv[2])


		

	print("now writing output to file", sys.argv[2])

	payments={}
	sums={}
	row=0
	index=l[row]
	row=+1

	while row <len(l):
		date=get_month(l[row][0])+"/"+get_year(l[row][0])
		payments[date]=[]
		sums[date]=0
		while row<len(l) and date==get_month(l[row][0])+"/"+get_year(l[row][0]):
			if l[row][7]=="Paid":
				value=float(l[row][3])
				payments[date].append(value)
				sums[date]+=value
			row+=1


			
	alpha1_large=0.029
	alpha1_small=0.029
	fix_cost=.3

	out1=model1(payments,sums,alpha1_large,alpha1_small,fix_cost)


	alpha2_large=0.003
	alpha2_medium=0.0025
	alpha2_small=0.002

	fix_cost_large=.2
	fix_cost_medium=.15
	fix_cost_small=.1

	out2=model2(payments,sums,alpha2_large,alpha2_medium,alpha2_small,fix_cost_large,fix_cost_medium,fix_cost_small)


	output.write("Month,Revenue,Cost,Floating fees\n")
	cost_of_operation=0
	for i in payments.keys():
		output.write(i+','+str(sums[i])+','+str(out1[i][1])+','+str(out1[i][0])+'\n')
		cost_of_operation+=out1[i][1]
	output.write('\nTotal cost:,'+str(cost_of_operation)+'\n\n')

	if out2==0:
		output.write('"You got under the limit scale to benefit from our plan, bye bye"')
	else:
		output.write('Month,Revenue,Cost,IC fee,IC fix,Floating fees,Floating fix cost\n')
		cost_of_operation=0
		for i in payments.keys():
			output.write(i+','+str(sums[i])+','+str(out2[i][3])+','+str(out2[i][0][0])+','+str(out2[i][0][1])+','+str(out2[i][1])+','+str(out2[i][2])+'\n')
			cost_of_operation+=out2[i][3]
		output.write('\nTotal cost:,'+str(cost_of_operation))


		


			
	output.write('\n\nEND')
		
	output.close

	#This part is written so that the excel code cannot pursue it's execution before python is done
	print("renaming ", sys.argv[3], "into ", sys.argv[4])
	os.rename(sys.argv[3], sys.argv[4])


	end=time.time()
	print("chrono= "+str(end-departure)+'s, or '+str(floor((end-departure)/60))+"m and "+str((end-departure)%60)+"s")	



	
