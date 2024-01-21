import os
import pandas as pd

def load_and_transform_data(input_folder, output_file):
    # Get a list of all files in the input folder
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Initialize an empty DataFrame to hold all the data
    all_data = pd.DataFrame()

    for file in files:
        # Determine the file extension
        _, file_extension = os.path.splitext(file)

        # Determine the appropriate engine
        if file_extension == '.xls':
            engine = 'xlrd'
        elif file_extension == '.xlsx':
            engine = 'openpyxl'
        else:
            continue  # Skip files with other extensions

        # Load the Excel file
        df = pd.read_excel(os.path.join(input_folder, file), engine=engine)

        # Define a dictionary of old column names to new column names
        columns_to_rename = {
            "Comment évalueriez-vous la qualité de votre travail pendant ce sprint ?": "Quality_Rating",
            "Comment évalueriez-vous la charge de travail de ce sprint ?": "Workload_Rating",
            "Comment évalueriez-vous votre niveau d'énergie à la fin de ce sprint ?": "Energy_Rating",
            "Comment évalueriez-vous le travail réalisé par vos collègues pendant ce sprint ?": "Colleagues_Rating",
            "Quelle note attribueriez-vous à ce sprint ?": "Sprint_Rating",
            "Start time": "Date",
            "Heure de début": "Date"
        }

        # Rename columns if they exist
        for old_name, new_name in columns_to_rename.items():
            if old_name in df.columns:
                df.rename(columns={old_name: new_name}, inplace=True)

        # Simplify the 'Start Time' column to keep only the date
        df['Date'] = pd.to_datetime(df['Date']).dt.date

        # Remove unnecessary columns
        columns_to_remove = ['Heure de fin', 'Adresse de messagerie', 'Nom', 'Langue', 'Completion time', 'Email', 'Name', 'Language', 'ID']
        for column in columns_to_remove:
            if column in df.columns:
                df.drop(column, axis=1, inplace=True)

        # Extract 'Year', 'Quarter', and 'Sprint_ID' from filename
        file_name = os.path.basename(file).split('.')[0]
        year, quarter, sprint_number = file_name.split('_')

        df['Year'] = year
        df['Quarter'] = quarter
        df['Sprint_ID'] = file_name.replace(' ', '_')

        # Append the transformed data to the all_data DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)

    # Sort the all_data DataFrame by the 'Start_Time' column
    all_data.sort_values('Date', inplace=True)

    # Write the all_data DataFrame to a CSV file
    all_data.to_csv(output_file, index=False)

# Call the function
load_and_transform_data('raw_data', 'clean_data/dataset.csv')