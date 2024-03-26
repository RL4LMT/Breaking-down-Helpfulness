import numpy as np
import pandas as pd
from statsmodels.stats import inter_rater as irr
from tabulate import tabulate

n = 60
#Keys are the annotators, values the columns required. since the relevance col are not independent we decide to keep only the performance one to have a general values considering also the relevances values remove the "not column.endswith('_relevance') and" from each
annotators = {
    "Darja": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-darja.csv", usecols=lambda column: not column.endswith('_relevance') and column != 'id').fillna(0).astype(int)[:n],
    "GiulioC": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-giulioc.csv", usecols=lambda column: not column.endswith('_relevance') and column != 'id').fillna(0).astype(int)[:n],
    "GiulioP": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-giuliop.csv", usecols=lambda column: not column.endswith('_relevance') and column != 'id').fillna(0).astype(int)[:n],
    "Kristin": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-kristin.csv", usecols=lambda column: not column.endswith('_relevance') and column != 'id').fillna(0).astype(int)[:n],
    "Zhuge": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-zhuge.csv", usecols=lambda column: not column.endswith('_relevance') and column != 'id').fillna(0).astype(int)[:n]
}
gen_kappa_values = {}
perf_kappa_values = {}
# Cohen's kappa values for each pair of annotators
for annotator1, df1 in annotators.items():
    for annotator2, df2 in annotators.items():        
        table = pd.crosstab(df1.values.flatten(), df2.values.flatten())
        kappa = irr.cohens_kappa(table, return_results=False)
        gen_kappa_values[annotator1, annotator2] = kappa
# Table representattion 
headers = ["name", "Darja", "GiulioC", "GiulioP", "Kristin", "Zhuge"]
data = []
for annotator1 in annotators.keys():
    row = [annotator1]
    for annotator2 in annotators.keys():
        row.append(round(gen_kappa_values[(annotator1, annotator2)], 2))
    data.append(row)
print(tabulate(data, headers=headers, tablefmt="grid"))

lower_triangle = np.tril([[gen_kappa_values[(a1, a2)] for a2 in annotators.keys()] for a1 in annotators.keys()],-1)
mean_kappa = np.mean(lower_triangle[np.nonzero(lower_triangle)])
print(f'The mean of the inner agreement is: {mean_kappa}')
