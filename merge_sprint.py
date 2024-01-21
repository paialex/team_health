import pandas as pd

# Load the datasets
average_dataset_path = 'clean_data/average_dataset.csv'
sprint_dataset_path = 'clean_data/sprint.csv'

average_dataset = pd.read_csv(average_dataset_path)
sprint_dataset = pd.read_csv(sprint_dataset_path)

# Merging the datasets on 'Sprint_ID'
merged_dataset = pd.merge(average_dataset, sprint_dataset, on='Sprint_ID', how='inner')

# Save the merged dataset to a new CSV file
output_file_path = 'clean_data/merged_dataset.csv'
merged_dataset.to_csv(output_file_path, index=False)

