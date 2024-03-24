import csv, json, re

PATH = "../../annotation/"
FILES = [
    "databricks-dolly-1500_darja.csv",
    "databricks-dolly-1500_giulioc.csv",
    "databricks-dolly-1500_giuliop.csv",
    "databricks-dolly-1500_kristin.csv",
    # "databricks-dolly-1500_zhuge.csv"
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
    
# Retrieve type task and add as column
data = json.load(open("merged_data_1500.json"))

for datapoint in annotation:
    id = int(datapoint[0])
    for entry in data:
        if entry["id"] == id:
             datapoint.append(entry["category"])
             break
        
with open("merged_annotation_"+str(len(annotation))+".csv", "w", encoding="utf-8") as out_file:
    
    csv.writer(out_file, lineterminator="\n").writerows([["id","structure","informativity","on-topic","correctness","category"]]+annotation)