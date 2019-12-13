import os
import glob
import pandas as pd

os.chdir('./data')

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_csv.to_csv('library.csv', index=False)