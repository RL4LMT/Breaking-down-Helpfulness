import numpy as np
import pandas as pd
from statsmodels.stats import inter_rater as irr
from tabulate import tabulate

n = 60
annotators = {
    "Darja": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-darja.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n],
    "GiulioC": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-giulioc.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n],
    "GiulioP": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-giuliop.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n],
    "Kristin": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-kristin.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n],
    "Zhuge": pd.read_csv(filepath_or_buffer="../annotation/databricks-dolly-60-zhuge.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n]
}
#"name":["Darja","GiulioC","GiulioP","Kristin", "Zhuge"]
kappa_values = {}
# Cohen's kappa values for each pair of annotators
for annotator1, df1 in annotators.items():
    for annotator2, df2 in annotators.items():        
        table = pd.crosstab(df1.values.flatten(), df2.values.flatten())
        kappa = irr.cohens_kappa(table, return_results=False)
        kappa_values[annotator1, annotator2] = kappa

headers = ["name", "Darja", "GiulioC", "GiulioP", "Kristin", "Zhuge"]
data = []
for annotator1 in annotators.keys():
    row = [annotator1]
    for annotator2 in annotators.keys():
        row.append(round(kappa_values[(annotator1, annotator2)], 2))
    data.append(row)
print(tabulate(data, headers=headers, tablefmt="grid"))