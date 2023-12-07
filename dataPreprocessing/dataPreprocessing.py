import pandas as pd

file_path = 'output_submissions_amateurroomporn_enriched.csv'

# Read the CSV file and use the first and second rows as column names
df = pd.read_csv(file_path, header=[0, 1])

filtered_df = df[~df[(' removed_by', '61')].isin(['removed', 'deleted', 'moderator'])].copy()
filtered_df.columns = filtered_df.columns.get_level_values(0).str.strip()

#get column names
column_names = filtered_df.columns.get_level_values(0)
data = filtered_df[column_names]

#timestamp in correct format
data['author_created_utc'] = pd.to_datetime(data['author_created_utc'], unit='s')

data = data[data['author'] != '[deleted]']
data.to_csv('output_reddit.csv')