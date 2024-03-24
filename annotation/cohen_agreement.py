import numpy as np
import pandas as pd
from statsmodels.stats import inter_rater as irr


n = 50
annotator_d = pd.read_csv("databricks-dolly-60-darja.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n]
annotator_gc = pd.read_csv("databricks-dolly-60-giulioc.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n]
annotator_gp = pd.read_csv("databricks-dolly-60-giuliop.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n]
annotator_k = pd.read_csv("databricks-dolly-60-kristin.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n]
annotator_z = pd.read_csv("databricks-dolly-60-zhuge.csv", usecols=lambda column: column != 'id').fillna(0).astype(int)[:n]


table_gpk = pd.crosstab(annotator_k.values.flatten(), annotator_gp.values.flatten())
k_giuliopkristin = irr.cohens_kappa(table_gpk, return_results=False)
table_gpd = pd.crosstab(annotator_d.values.flatten(), annotator_gp.values.flatten())
k_giuliopdarja = irr.cohens_kappa(table_gpd, return_results=False)
table_gcgp = pd.crosstab(annotator_gp.values.flatten(), annotator_gc.values.flatten())
k_giulios = irr.cohens_kappa(table_gcgp, return_results=False)
table_gck = pd.crosstab(annotator_k.values.flatten(), annotator_gc.values.flatten())
k_giuliockristin = irr.cohens_kappa(table_gck, return_results=False)
table_gcd = pd.crosstab(annotator_d.values.flatten(), annotator_gc.values.flatten())
k_giuliocdarja = irr.cohens_kappa(table_gcd, return_results=False)
table_kd = pd.crosstab(annotator_k.values.flatten(), annotator_d.values.flatten())
k_darjakristin = irr.cohens_kappa(table_kd, return_results=False)

table_dd = pd.crosstab(annotator_d.values.flatten(), annotator_d.values.flatten())
k_darjadarja = irr.cohens_kappa(table_dd, return_results=False)

table_dz = pd.crosstab(annotator_d.values.flatten(), annotator_z.values.flatten())
k_darjazhuge = irr.cohens_kappa(table_dz, return_results=False)
table_gcz = pd.crosstab(annotator_gc.values.flatten(), annotator_z.values.flatten())
k_giulioczhuge = irr.cohens_kappa(table_gcz, return_results=False)
table_gpz = pd.crosstab(annotator_gp.values.flatten(), annotator_z.values.flatten())
k_giuliopzhuge = irr.cohens_kappa(table_gpz, return_results=False)
table_kz = pd.crosstab(annotator_k.values.flatten(), annotator_z.values.flatten())
k_kristinzhuge = irr.cohens_kappa(table_kz, return_results=False)

annotators_data = {
    "Darja": [1, k_giuliocdarja, k_giuliopdarja, k_darjakristin,k_darjazhuge],
    "GiulioC": [k_giuliocdarja, 1, k_giulios, k_giuliockristin,k_giulioczhuge],
    "GiulioP": [k_giuliopdarja, k_giulios, 1, k_giuliopkristin,k_giuliopzhuge],
    "Kristin": [k_darjakristin, k_giuliockristin, k_giuliopkristin, 1,k_kristinzhuge],
    "Zhuge": [k_darjazhuge, k_giulioczhuge, k_giuliopzhuge, k_kristinzhuge,1]
}

#Labeled annotators dataframe
annotators_df = pd.DataFrame(annotators_data, index=["Darja", "GiulioC", "GiulioP", "Kristin", "Zhuge"])
print(annotators_df)
mean_cohens_kappa = annotators_df.values[np.tril_indices_from(annotators_df, k=-1)].mean()

print("Mean Cohen's kappa between all annotators:", mean_cohens_kappa)

#test on annotator on itself
for col in annotator_gp.columns:
    table = pd.crosstab(annotator_gp[col], annotator_gp[col])
    #print(table)
    if table.size ==  1:
        k = 1.0
    else:
        k = irr.cohens_kappa(table, return_results=False)
    #print(k) #uncomment to check the total agreement


for col in annotator_gp.columns:
    if col.endswith("relevance"):
        table = pd.crosstab(annotator_gc[col], annotator_k[col])
        print(table)
        if table.size ==  1:
            k = 1.0
        else:
            k = irr.cohens_kappa(table, return_results=False)
    print(k) #uncomment to check the total agreement
