import json
import random
import csv
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
