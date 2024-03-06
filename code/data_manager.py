import json
import random
import csv
import os
import pandas as pd
from collections import Counter

# load the dataset
data = []
with open("data\databricks-dolly-15k.jsonl") as f:
        for line in f:
            json_object = json.loads(line)
            data.append(json_object)

# keep only 3 chosen categories
chosen = ['summarization', 'closed_qa', 'brainstorming']
filtered_data = [item for item in data if item.get('category') in chosen]

# add IDs
filtered_data = [{'id': i + 1, **item} for i, item in enumerate(filtered_data)]

# make sure that categories are equally distributed
counts = Counter(item['category'] for item in filtered_data)
min_count = min(counts.values())
equal_data = [
    item for category in chosen
    for item in random.sample([item for item in filtered_data if item['category'] == category], min_count)
]

# shuffle the data
random.seed(42)
random.shuffle(filtered_data)

# create a small subset of 60 items for common annotation
small_subset = []
for cat in chosen:
    items = [item for item in filtered_data if item['category'] == cat]
    small_subset.extend(items[:20])
random.shuffle(small_subset)    

with open('data\\databricks-dolly-60.json', 'w') as f:
    json.dump(small_subset, f, default=str, indent=2)


ids = [item['id'] for item in small_subset]

# add IDs 
csv_path = 'annotation\databricks-dolly-60-name.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
        'id', 'length_relevance', 'length_perfomance', 'structure_relevance', 'structure_perfomance',
        'informativity_relevance', 'informativity_perfomance', 'manner_relevance', 'manner_perfomance',
        'coherence_relevance', 'coherence_perfomace', 'evidence_relevance', 'evidence_perfomance',
        'correctness_relevance', 'correctness_perfomance', 'certainty_relevance', 'certainty_perfomance']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for _id in ids:
            writer.writerow({'id': _id})

def modify_csv_files(folder_path):
    # remove columns
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    columns = ['length_relevance','length_perfomance','manner_relevance','manner_perfomance','certainty_relevance','certainty_perfomance']
    for file in files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df = df.drop(columns=columns, errors='ignore')

        # rename coherence -> on-topic
        if 'coherence_relevance' in df.columns:
            df = df.rename(columns={'coherence_relevance': 'on-topic_relevance'})
        if 'coherence_perfomace' in df.columns:   
           df = df.rename(columns={'coherence_perfomace': 'on-topic_perfomace'})

        # overwrite
        df.to_csv(file_path, index=False)

if __name__ == "__main__":
    folder_path = 'C:/Users/User/Documents/UNI/WiSe_2023/RL/Project/annotation'
    modify_csv_files(folder_path)