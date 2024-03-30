import csv, json, re

# PATH = "../../annotation/"
PATH = "annotation/"

# FILES = [
#     "databricks-dolly-1500_darja.csv",
#     "databricks-dolly-1500_giulioc.csv",
#     "databricks-dolly-1500_giuliop.csv",
#     "databricks-dolly-1500_kristin.csv",
#     "databricks-dolly-1500_zhuge.csv"
# ]

FILES = [
    "llama13bchat_responses_databricks-dolly-30_darja.csv",
    "llama13bchat_responses_databricks-dolly-30_giulioc.csv",
    "llama13bchat_responses_databricks-dolly-30_giuliop.csv",
    "llama13bchat_responses_databricks-dolly-30_kristin.csv",
    "llama13bchat_responses_databricks-dolly-30_zhuge.csv",
]

merged_annotation = []
for file in FILES:
    with open(PATH+file, encoding="utf-8") as data:
        entries = csv.reader(data)
        next(entries)
        for entry in entries:
            if re.match(r"\d+,[0-4],[0-4],[0-4],[0-4]", ",".join(entry)):
                merged_annotation.append(entry)

annotation = sorted(merged_annotation, key=lambda x: int(x[0])) 

# for the extra two columns for model answer
new_annotation = []
for inner in annotation:
    if len(inner) == 6:
        new_annotation.append(inner[:-1])
    else:
        new_annotation.append(inner[:-2])

# Retrieve type task and add as column
data = json.load(open("merged_data_1500.json"))

for datapoint in new_annotation:
    id = int(datapoint[0])
    for entry in data:
        if entry["id"] == id:
             datapoint.append(entry["category"])
             break

# with open("merged_annotation_"+str(len(annotation))+".csv", "w", encoding="utf-8") as out_file:
    
#     csv.writer(out_file, lineterminator="\n").writerows([["id","structure","informativity","on-topic","correctness","category"]]+annotation)

with open("merged_llama_annotation_"+str(len(new_annotation))+".csv", "w", encoding="utf-8") as out_file:
    
    csv.writer(out_file, lineterminator="\n").writerows([["id","structure","informativity","on-topic","correctness","category"]]+new_annotation)