import json, re

PATH = "../../data/"
FILES = [
    "databricks-dolly-1500_darja.json",
    "databricks-dolly-1500_giulioc.json",
    "databricks-dolly-1500_kristin.json",
    "databricks-dolly-1500_giuliop.json",
    "databricks-dolly-1500_zhuge.json"
]

merged = []
for file in FILES:
    with open(PATH+file, encoding="utf-8") as data:
        merged += json.load(data)

merged = sorted(merged, key=lambda x: int(x["id"]))

print(len(merged))

with open("merged_data_"+str(len(merged))+".json", "w", encoding="utf-8") as out_file:
    json.dump(merged, out_file, indent=1)