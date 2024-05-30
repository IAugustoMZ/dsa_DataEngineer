#%%
import os
import ast
import glob
import warnings
import numpy as np
import pandas as pd


# ignore warnings
warnings.filterwarnings("ignore")

# define the path to the data source
source_path = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    ),
    'data',
    'safety_datasets'
)


# define the sink path
sink_path = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
        ),
    ),
    'iac',
    'data'
)
sink_name ='dataset.csv'

# read the data
# get a list of all CSV files in the folder
csv_files = glob.glob(os.path.join(source_path, '*.csv'))

# create an empty list to store the dataframes
dfs = []

# iterate over each CSV file
for file in csv_files:
    # read the CSV file into a dataframe
    df = pd.read_csv(file)
    # append the dataframe to the list
    dfs.append(df)

# concatenate all dataframes into a single dataframe
data = pd.concat(dfs, ignore_index=True)

# drop unused columns
data.drop(columns=['issues'], inplace=True)

# since the data frame has small size, we can use a loop for
data_final = {
    'reports': [],
    'severities': []
}
for i, row in data.iterrows():

    # get the reports
    data_final['reports'] += ast.literal_eval(row['reports'])

    # get the label
    data_final['severities'] += list(np.repeat(row['severities'], repeats=len(ast.literal_eval(row['reports']))))

# create the dataframe
data_final = pd.DataFrame.from_dict(data_final, orient='columns')

# save the data
data_final.to_csv(os.path.join(sink_path, sink_name), index=False)