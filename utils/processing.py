import os
import json
import numpy as np
import pandas as pd

class Process:
    def __init__(self):
        self.locs = dict()  # Will contain all locations (str) and corresponding coordinates
        self.cwd = os.getcwd()


    def get_crds(self, name):
        """Extracts lat & lon from filename"""

        coords = name.split('_')
        lat = float(coords[1])
        lon = float(coords[2])

        return [lon, lat]

    def process(self):
        # Concatenate each location into one file
        for loc in os.listdir(f'{self.cwd}/data/raw/'):
            sub_dir_name = os.path.join(f'{self.cwd}/data/raw/', loc)
            L = len(os.listdir(sub_dir_name))  # Number of files for location
            for i, file in enumerate(os.listdir(sub_dir_name)):
                name = os.fsdecode(file)  # Just the filename, not the dir
                df = pd.read_csv(f'{sub_dir_name}/{name}',
                                skiprows=2)
                # Last column just contains NA values
                df.drop(df.columns[len(df.columns)-1],
                        axis=1,
                        inplace=True)

                # Is only run the first time for each location
                if i == 0:
                    locs[loc] = self.get_crds(name)

                    N = df.shape[0]
                    arr = np.zeros((N*L, df.shape[1]))  # Preallocating for speed
                    cols = list(df.columns.str.lower())  # Extracting the column names
                    df_new = pd.DataFrame(arr, columns=cols)  # Preallocating for speed

                df_new.iloc[i*N:(i+1)*N, :] = df.values  # Filling in the dataframe

            # WARNING: Takes a few mins to run
            df_new.to_csv(f'data/processed/{loc}.zip',
                        index=False,
                        compression="zip")

        # Save location and coordinates to be loaded later
        with open(f'{self.cwd}/utils/location.json', 'w') as f:
            json.dump(locs, f)

if __name__ == '__main__':
    with Process as proc:
        proc.process()
