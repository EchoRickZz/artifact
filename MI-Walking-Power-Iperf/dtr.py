# !/usr/bin/python

# Decision Tree regression

# Usage: python dtr.py -d [training data path] -k [keyword in filenames] -s [optional, save the improved model]

import numpy as np
import pandas as pd
import sys
import os
import pickle
import argparse
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, SCORERS
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.tree import DecisionTreeRegressor

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--data", help = "path to the training data")
ap.add_argument("-k", "--keyword", help = "keyword in the log names")
ap.add_argument("-s", "--save", help = "save model to disk")
args = vars(ap.parse_args())

path = args["data"]
files = [x for x in os.listdir(path) if 'csv' in x]
if args["keyword"]:
	keyword = args["keyword"]
	files = [x for x in files if keyword in x and 'lock' not in x]
print(files)

df_list = []
for file in files:
    tmp = pd.read_csv(path + '/' + file, header=None)
    # tmp = pd.read_csv(path + '/' + file, sep='\t', encoding='utf-16', header=None)
    df_list.append(tmp)
    # print(tmp.head(), tmp.size)
df = pd.concat(df_list, ignore_index=True)
# df.columns = ["TS", "STATUS", "LTE_RSRP", "RSRP", "SINR", "CPU_TEMP", "BATTERY_TEMP", "DL", "UL", "SW_POWER", "POWER", "POWER_FULL"]
df.columns = ["TS", "STATUS", "LTE_RSRP", "RSRP", "SINR", "DL", "UL", "SW_POWER", "POWER", "POWER_FULL"]
# df.columns = ["RSRP", "POWER_FULL", "STATUS", "DL", "LTE_RSRP", "SINR", "POWER", "SW_POWER", "TS", "UL"]
# df = pd.read_csv(args["data"], header = None)
# print(df.head())
print(f"Shape: {df.shape}")

df_train, df_test = train_test_split(df, train_size = 0.7, test_size = 0.3, random_state = 5)


X_column = ["RSRP", "DL", "UL"]
# X_column = ["RSRP"]
# X_column = ["DL", "UL"]

# X_column = ["RSRP", "DL", "UL", "SW_POWER"]
# X_column = ["SW_POWER"]
print(X_column)

Y_column = ["POWER_FULL"]

X = df[X_column].to_numpy()
Y = df[Y_column].to_numpy().reshape(-1)

# idx = np.where(X[:,1]>1400)
# X = X[idx]
# Y = Y[idx]
# print(X.shape, Y.shape)


X_train = df_train[X_column].to_numpy()
Y_train = df_train[Y_column].to_numpy().reshape(-1)


regr_dep2 = DecisionTreeRegressor(max_depth=2)
regr_dep3 = DecisionTreeRegressor(max_depth=3)
regr_dep4 = DecisionTreeRegressor(max_depth=4)
regr_dep5 = DecisionTreeRegressor(max_depth=5)
regr_dep6 = DecisionTreeRegressor(max_depth=6)
regr_dep7 = DecisionTreeRegressor(max_depth=7)
regr_dep8 = DecisionTreeRegressor(max_depth=8)
regr_dep9 = DecisionTreeRegressor(max_depth=9)
regr_dep10 = DecisionTreeRegressor(max_depth=10)
dtrs = [
		# regr_dep2, 
		# regr_dep3, 
		# regr_dep4, 
		regr_dep5, 
		regr_dep6, 
		regr_dep7, 
		regr_dep8, 
		# regr_dep9, 
		# regr_dep10
		]
kernel_label = [
		# 'DTR_2', 
		# 'DTR_3', 
		# 'DTR_4', 
		'DTR_5',
		'DTR_6', 
		'DTR_7',
		'DTR_8', 
		# 'DTR_9', 
		# 'DTR_10'
		]

Y_mean = df[Y_column[0]].mean()
Y_max = df[Y_column[0]].max()
print(f"Y_mean: {Y_mean}, Y_max: {Y_max}")

for i in range(len(dtrs)):
	dtr = dtrs[i]
	label = kernel_label[i]
	X_test = df_test[X_column]
	Y_test = df_test[Y_column]
	model = dtr.fit(X_train, Y_train)
	Y_pred = model.predict(X_test)

	if args["save"]:
		pkl_filename = args["save"]
		with open(pkl_filename, 'wb') as file:
			pickle.dump(model, file)

	mae = mean_absolute_error(Y_test, Y_pred)
	mse = mean_squared_error(Y_test, Y_pred)
	rmse = np.sqrt(mse)
	r2 = r2_score(Y_test, Y_pred)
	score = model.score(X_test, Y_test)

	
	Y_test = Y_test.to_numpy().reshape(-1)


	# plot errors vs. ul, errors vs. dl

	errors = np.abs(Y_test-Y_pred)/Y_test
	X_Y_errors = np.hstack((X_test, Y_test.reshape(-1,1), Y_pred.reshape(-1,1), errors.reshape(-1,1)))
	print(errors.mean())

	# print(f"{mae}")
	# print(f"{rmse}")
	# print(f"{score}")
	# for i in SCORERS.keys():
	# 	print(i)

	scores = cross_val_score(model, X, Y, cv=10, scoring='neg_mean_absolute_percentage_error') #  
	print(f"{np.abs(scores.mean())}\t{scores.std()}")  # mae

	# predictions = cross_val_predict(model, X, Y, cv=10)
	scores = cross_val_score(model, X, Y, cv=10, scoring='r2') 
	print(f"{np.abs(scores.mean())}\t{scores.std()}\n")  # score
