import numpy as np
import pandas as pd
from statsmodels.stats import inter_rater as irr
from tabulate import tabulate

n = 60
names = ["darja","giulioc","giuliop","kristin","zhuge"]
annotators = {}
for name in names:
    annotators[name.capitalize()] = pd.read_csv(filepath_or_buffer=f"../annotation/databricks-dolly-60-{name}.csv", usecols=lambda column: not column.endswith('_relevance') and column != 'id').fillna(0).astype(int)[:n]

gen_kappa_values = {}
# Cohen's kappa values for each pair of annotators
for annotator1, df1 in annotators.items():
    for annotator2, df2 in annotators.items():        
        table = pd.crosstab(df1.values.flatten(), df2.values.flatten())
        kappa = irr.cohens_kappa(table, return_results=False)
        gen_kappa_values[annotator1, annotator2] = kappa

# table representtation 
headers = ["General_Agreement", "Darja", "Giulioc", "Giuliop", "Kristin", "Zhuge"]
data = []
for annotator1 in annotators.keys():
    row = [annotator1]
    for annotator2 in annotators.keys():
        row.append(round(gen_kappa_values[(annotator1, annotator2)], 2))
    data.append(row)
print(tabulate(data, headers=headers, tablefmt="grid"))

# compute mean  
lower_triangle = np.tril([[gen_kappa_values[(a1, a2)] for a2 in annotators.keys()] for a1 in annotators.keys()],-1)
mean_kappa = np.mean(lower_triangle[np.nonzero(lower_triangle)])
print(f'Mean: {mean_kappa}')

score = {}
# perform crosstab between two columns from the DataFrames
for c in annotators[names[0].capitalize()].columns:
    score_d = {}
    for annotator1, data1 in annotators.items():
        for annotator2, data2 in annotators.items():    
            crosstab_result = pd.crosstab(data1[c], data2[c])
            
            #reshape the table
            reshaped_index = range(5)
            reshaped_crosstab = pd.DataFrame(0, index=reshaped_index, columns=reshaped_index)
            # update values from the crosstab result
            for index, row in crosstab_result.iterrows():
                for col, value in row.items():
                    reshaped_crosstab.at[index, col] = value
            
                # extra: fillwith zeros
                reshaped_crosstab.fillna(0, inplace=True)
            
            
            score_d[annotator1, annotator2] = irr.cohens_kappa(reshaped_crosstab, return_results=False )
    score[c] = score_d

for component, score_dict in score.items():
    #print(component)
    headers = [f"{component}", "Darja", "Giulioc", "Giuliop", "Kristin", "Zhuge"]
    data = []
    for a1 in annotators.keys():
        row = [a1]
        for a2 in annotators.keys():
            row.append(round(score_dict[(a1,a2)],2))
        data.append(row)
    print(tabulate(data, headers=headers, tablefmt="grid"))
    # compute mean  
    lower_triangle = np.tril([[score_dict[(a1, a2)] for a2 in annotators.keys()] for a1 in annotators.keys()],-1)
    mean_kappa = np.mean(lower_triangle[np.nonzero(lower_triangle)])
    print(f'Mean: {mean_kappa}')
