import pandas as pd
#import chardet

df = pd.read_csv('GroceryStore.csv')

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

whole_foods = df[df['STORE NAME'].str.contains("WHOLE")]
aldi = df[df['STORE NAME'].str.contains("ALDI")]

def plot_whole_foods():
	plt.scatter(whole_foods.LATITUDE, whole_foods.LONGITUDE, color='r')

def plot_aldi():
	plt.scatter(aldi.LATITUDE, aldi.LONGITUDE, color='b')

def replace_store(full_df, substring, replacement):
	for index, row in full_df.iterrows():
		#print(row['STORE NAME'])
		if substring in row['STORE NAME']:
			#print("found a jewel")
			#print(row['STORE NAME'])
			full_df.at[index, 'STORE NAME'] = replacement
	return full_df

def is_liquor_store(full_df):
	for index, row in full_df.iterrows():
		#print(row['STORE NAME'])
		if "LIQUOR" in row['STORE NAME']:
			#print("found a jewel")
			#print(row['STORE NAME'])
			full_df['LIQUOR STORE'] = 1
		else:
			full_df['LIQUOR STORE'] = 0
	return full_df

def clean_df(full_df):
	full_df = replace_store(full_df, "EWEL", "JEWEL")
	full_df = replace_store(full_df, "LDI", "ALDI")
	full_df = replace_store(full_df, "ALGREEN", "WALGREENS")
	full_df = replace_store(full_df, "SAVE-A", "SAVE-A-LOT")
	full_df = replace_store(full_df, "TRADER", "TRADER JOE'S")
	full_df = replace_store(full_df, "4 LESS", "FOOD 4 LESS")
	full_df = replace_store(full_df, "ALMAR", "WALMART")
	full_df = replace_store(full_df, "WHOLE", "WHOLE FOODS")
	full_df = is_liquor_store(full_df)
	return full_df

neighborhood_gb = df.groupby('COMMUNITY AREA NAME')
neighborhood_gb['STORE NAME'].value_counts()

neighborhood_gb.get_group('LAKE VIEW')['STORE NAME'].value_counts()

gcfd = pd.read_csv('gcfd_programs.csv', encoding = "ISO-8859-1")

gcfd = gcfd.dropna(subset=['Community Area'])
gcfd['Community Area'] = gcfd['Community Area'].str.upper()

# something is not right with the merge, numbers are too high
merged_df = pd.merge(df, gcfd, left_on='COMMUNITY AREA NAME', right_on='Community Area', how='outer')
gb_neighbrood_merged = merged_df.groupby('COMMUNITY AREA NAME')

### interesting breakdowns
gcfd_neighborhood = gcfd.groupby('Community Area')


gcfd_neighborhood['Program Type'].value_counts()
neighborhood_gb['STORE NAME'].value_counts()

# Do df = make_long_table()
def make_long_table():
	df = pd.read_csv('GroceryStore.csv')
	gcfd = pd.read_csv('gcfd_programs.csv', encoding = "ISO-8859-1")
	df = clean_df(df)
	gcfd = gcfd.dropna(subset=['Community Area'])
	gcfd['Community Area'] = gcfd['Community Area'].str.upper()
	socio_df = pd.read_csv('SocioeconomicData.csv')

	socio_df=socio_df.rename(columns={'COMMUNITY AREA NAME':'Community Area'})

	socio_df['Community Area'] = socio_df['Community Area'].str.upper()
	socio_df_hardship = socio_df[['Community Area', 'HARDSHIP INDEX']]


	# School Data
	school_df = pd.read_csv('community_school_meal_participation.csv')
	school_df['Community Area'] = school_df['Community Area'].str.upper()
	school_df_sub = school_df[['Community Area', 'Normalized Eligible Children (#Eligible/Total # Eligible)', 'Percentage of children eligible for free and reduced price meals, 2016' ]]
	school_df_sub = school_df_sub.rename(columns = {'Percentage of children eligible for free and reduced price meals, 2016': 'Reduced Meal Eligibiity'})
	school_df_sub = school_df_sub.rename(columns = {'Normalized Eligible Children (#Eligible/Total # Eligible)': 'Normalized Reduced Meal Eligiblity'})

	# subset
	store_df= df[['COMMUNITY AREA NAME', 'STORE NAME', 'LATITUDE', 'LONGITUDE']]
	store_df=store_df.rename(columns = {'COMMUNITY AREA NAME':'Community Area'})
	gcfd_sub = gcfd[['Community Area', 'Program Name', 'Program Type', 'Activity Status']]
	concated = pd.concat([store_df, gcfd_sub, socio_df_hardship, school_df_sub], ignore_index=True)

	df_reorder = concated[['Community Area', 'STORE NAME', 'Program Name', 'Program Type', 'Activity Status','Reduced Meal Eligibiity', 'Normalized Reduced Meal Eligiblity', 'HARDSHIP INDEX', 'LATITUDE', 'LONGITUDE']]

	return df_reorder

def filter_by_hardship_high(df, hardship_thresh):
	hardship_df = df[df['HARDSHIP INDEX'] > hardship_thresh]
	return hardship_df

def filter_by_hardship_low(df, hardship_thresh):
	hardship_df = df[df['HARDSHIP INDEX'] < hardship_thresh]
	return hardship_df

def filter_by_community_area(df, name):
	community = df[df['Community Area'] == name]
	return community




