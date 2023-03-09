import os
from shutil import rmtree
import pandas as pd
import geopandas as gpd

# Declare relevant dirs
header_dir = "./data/sample/headers"
raw_dir = "./data/raw"
csv_dir = "./data/processed/csv"

# Defines columns that are necessary and/or significant
critical = ['Longitude', 'Latitude', 'Field', 'Product', 'Date',
	'Elevation(ft)', 'Yld Mass(Dry)(lb/ac)']

# Defines columns to sort output CSVs by
sort_by = ['Year', 'Field', 'Product']

# Create dict of column header templates from samples for data types
types = {}
for (root, dirs, files) in os.walk(header_dir):
	for file in files:
		# Determine data type from file name
		type_name = file[:len(file) - file[::-1].index("_") - 1]

		if type_name not in types:
			types[type_name] = {'headers': [], 'files': []}

		# Attempting reading using different codecs
		for codec in ['utf8', 'ISO-8859-1', 'ascii']:
				try:
					# Add to appropriate list
					df = pd.read_csv(root + "/" + file, encoding = codec)
					types[type_name]['headers'].append(df.columns)
					break
				except:
					pass

# Create a list of all field boundaries
boundary_files = []
for (root, dirs, files) in os.walk(raw_dir):
	for file in files:
		if (file.endswith(".shp")):
			path = root + "/" + file

			# Read in shape file, only using 'Field' and 'geometry' columns
			boundary_files.append(gpd.read_file(path)[['Field', 'geometry']])

# Combine all boundaries into one table
boundaries = pd.concat(boundary_files, ignore_index = True)

# Read in all CSVs and categorize them by column header
for (root, dirs, files) in os.walk(raw_dir):
	for file in files:
		if (file.endswith(".csv")):
			# Attempting reading using different codecs
			for codec in ['ISO-8859-1', 'utf8', 'ascii']:
				try:
					path = root + "/" + file
					df = pd.read_csv(path, encoding = codec, low_memory = False)

					# Match up file to data type (or multiple)
					for t in types:
						for header in types[t]['headers']:
							if len(df.columns) == len(header):
								if all(df.columns == header):
									types[t]['files'].append(df)
									matched = True

					if not matched:
						print("Unmatched file. Columns headers unknown.")

					break
				except:
					pass

# Concat all tables within each type, then clean the combined dataframe
for t in types:
	if len(types[t]['files']) > 0:
		df = pd.concat(types[t]['files'], ignore_index = True)

		# Drop rows missing critical values
		df.dropna(subset = critical, inplace = True)
		df = df[df['Product'] != 'NO Product']

		# Drop any duplicate data
		df.drop_duplicates()

		# Add a 'Year' value for later categorization
		df['Year'] = [int(date[-4:]) for date in df['Date']]

		# Correct field attribute based on long/lat data
		geometry = gpd.points_from_xy(x = df.Longitude, y = df.Latitude)
		gdf = gpd.GeoDataFrame(df, crs = 'EPSG:4326', geometry = geometry)
		df = pd.DataFrame(gpd.sjoin(gdf, boundaries))
		df['Field_left'] = df['Field_right']
		df.drop(['geometry', 'Field_right', 'index_right'], axis = 1,
			inplace = True)
		df.rename(columns = {'Field_left': 'Field'}, inplace = True)

		types[t]['together'] = df

# Make/clean folders and store data by year, field, and product
for t in types:
	if 'together' in types[t]:
		path = csv_dir + "/" + t

		# Delete folder if it exists
		if os.path.exists(path):
			rmtree(path)
		os.mkdir(path)

		holding = [types[t]['together']]

		# Create list of all data broken up by the categories in sort_by
		for field in sort_by:
			temp = []

			for table in holding:
				for value in table[field].unique():
					temp.append(table[table[field] == value])

			holding = temp

		# Write each table to file, using categories to name the file
		for table in holding:
			file_name = ""
			for field in sort_by:
				field_value = str(table[field].values[0])
				field_value = field_value.replace("/", "-")
				field_value = field_value.replace("\\", "-")
				field_value = field_value.replace("_", "-")
				file_name += field_value + "_"
			file_name = file_name[:-1] + ".csv"

			# Remove 'Year' column as it was not in the original data
			table.drop('Year', axis = 1, inplace = True)

			table.to_csv(path + "/" + file_name, index = False)
