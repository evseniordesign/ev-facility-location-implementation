import numpy as np
import mapping.cost_gen as cg

MEANS = [4841, .236, 35.18, .495, .119, 2.77, .248, 3103, .783, 66416, .186, .144, .645, 1200.1] 
STDDEVS= [2450, 0.059, 6.652, 0.033, .164, .5 ,.191, 3288, 0.091, 36273, .166, .124, .229, 1379.2]

def get_gamma_params(mean, var):
	theta = var/mean
	k = mean/theta

	return k, theta

def generate_tract():
	tract = []
	for mean, sd in zip(MEANS, STDDEVS):
		k, theta = get_gamma_params(mean, sd*sd)
		estimate = np.random.gamma(k, theta, 1)[0]
		tract.append(estimate)
	return tract

def predict_EVCount():
	tract = generate_tract()
	print("Population: " + str(tract[0]))
	print("Age Below 16 Fraction: " + str(tract[1]))
	print("Median age: " + str(tract[2]))
	print("Male Fraction: " + str(tract[3]))
	print("African American Fraction: " + str(tract[4]))
	print("Average Houshold Size: " + str(tract[5]))
	print("Fraction with at Least Bachelor's: " + str(tract[6]))
	print("Population density: " + str(tract[7]))
	print("Fraction of workers Commuting by driving: " + str(tract[8]))
	print("Mean household income: " + str(tract[9]))
	print("Fraction of $100K+ income: " + str(tract[10]))
	print("Fraction of poverty: " + str(tract[11]))
	print("Land Use Balance: " + str(tract[12]))
	print("Employment Dennsity per sq mile: " + str(tract[13]))

	print(" ")

	count = cg.get_evcount(tract)
	print("EV COUNT: " + str(count))

