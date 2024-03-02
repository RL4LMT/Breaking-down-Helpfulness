import json
import random
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
for i, item in enumerate(filtered_data):
    item['id'] = i + 1  

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

with open('data\\databricks-dolly-50.json', 'w') as f:
    json.dump(small_subset, f, default=str, indent=2)