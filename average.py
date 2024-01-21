import pandas as pd

# Load the dataset
dataset_path = 'clean_data/dataset.csv'  # Replace with your actual file path
dataset_df = pd.read_csv(dataset_path)

# Grouping by Sprint_ID and calculating the required statistics
grouped_df = dataset_df.groupby('Sprint_ID').agg(
    {'Date': pd.Series.mode,
     'Year': pd.Series.mode,
     'Quarter': pd.Series.mode,
     'Quality_Rating': ['min', 'mean', 'max'], 
     'Workload_Rating': ['min', 'mean', 'max'], 
     'Energy_Rating': ['min', 'mean', 'max'], 
     'Colleagues_Rating': ['min', 'mean', 'max'], 
     'Sprint_Rating': ['min', 'mean', 'max'],
     'Sprint_ID': 'size'
    }
)

# Flattening the MultiIndex in columns created by the agg method
grouped_df.columns = ["_".join(x) if x[1] != '' else x[0] for x in grouped_df.columns]

# Renaming columns to make them more readable
grouped_df.rename(columns={
    'Date_': 'Date',
    'Year_': 'Year',
    'Quarter_': 'Quarter',
    'Sprint_ID_size': 'Participants_Count'
    }, inplace=True)

# Resetting index to include Sprint_ID as a column
grouped_df = grouped_df.reset_index()

# Round the average values to two decimal places
grouped_df = grouped_df.round(2)

# After the operation that changes 'Date' to 'Date_mode'
grouped_df.rename(columns={'Date_mode': 'Date'}, inplace=True)

# Save the transformed dataset to a CSV file
average_csv_path = 'clean_data/average_dataset.csv'  # Replace with your desired file path
grouped_df.to_csv(average_csv_path, index=False)
