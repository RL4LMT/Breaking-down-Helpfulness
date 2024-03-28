import json
import random
import csv
import os
import pandas as pd
from collections import Counter

# helper methods


def reduce_components_column(input_file, output_file):
    # can only run this once, remember to backup your file
    df = pd.read_csv(input_file)
    df.drop(['evidence_relevance', 'evidence_perfomance'], axis=1, inplace=True)
    relevance_columns = [col for col in df.columns if col.endswith('_relevance')]
    df.drop(relevance_columns, axis=1, inplace=True)
    # just noticed that there were typos in the colum title 'perfomance' and 'perfomace'
    df.rename(columns=lambda x: x.replace('_perfomance', ''), inplace=True)
    df.rename(columns=lambda x: x.replace('_perfomace', ''), inplace=True)

    df.to_csv(output_file, index=False)


def count_categories(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    data_length = len(data)
    category_counts = Counter(item['category'] for item in data)

    return data_length, category_counts


def write_csv_with_ids(json_file, csv_file):
    header = ['id', 'structure', 'informativity', 'on-topic', 'correctness', 'usefulness'] # modify header if needed
    with open(json_file, 'r') as file:
        data = json.load(file)
    ids = [item['id'] for item in data]
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for data_id in ids:
            writer.writerow({'id': data_id})


def find_category(json_data, question_id):
    category = ""
    for item in json_data:
        if item['id'] == question_id:
            category = item.get('category')
    return category


def retrieve_json_data(json_data_dict, selected_questions_dict):
    retrieved_data = {}
    for file_name, category_data in selected_questions_dict.items():
        retrieved_data[file_name] = {}
        for category, ids in category_data.items():
            retrieved_data[file_name][category] = []
            json_data = json_data_dict[file_name]
            for id in ids:
                for item in json_data:
                    if item['id'] == id:
                        retrieved_data[file_name][category].append(item)
                        break
    return retrieved_data


def load_json_data(json_directory, file_name_common_string):
    json_data_dict = {}
    json_paths = os.listdir(json_directory)

    json_files = [file for file in json_paths if file.startswith(file_name_common_string) and file.endswith(".json")]

    for file in json_files:
        file_path = os.path.join(json_directory, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
            json_data_dict[file.replace(".json", "")] = data
    return json_data_dict


def save_json_data(json_data, file_name):
    with open("../data/"+file_name + ".json", "w") as f:
        json.dump(json_data, f, indent=4)


def select_questions_for_llm_response(json_directory, csv_directory):
    files = os.listdir(csv_directory)

    csv_files = [file for file in files if file.startswith("databricks-dolly-1500_") and file.endswith(".csv")]

    csv_data_dict = {}

    for file in csv_files:
        file_path = os.path.join(csv_directory, file)
        data = pd.read_csv(file_path)
        csv_data_dict[file.replace(".csv", "")] = data

    json_data_dict = load_json_data(json_directory, "databricks-dolly-1500_")

    selected_questions_dict = {}

    for file_name in csv_data_dict.keys():
        selected_questions_dict[file_name] = {}
        filtered_data = csv_data_dict[file_name].dropna(subset=['structure', 'informativity', 'on-topic', 'correctness'])
        for category in ['summarization', 'closed_qa', 'brainstorming']:
            category_ids = set()
            while len(category_ids) < 10:
                random_row = filtered_data.sample(n=1)
                random_id = random_row['id'].iloc[0]
                json_data = json_data_dict[file_name]
                cat = find_category(json_data, random_id)
                if cat == category:
                    category_ids.add(random_id)

            selected_questions_dict[file_name][category] = category_ids

    retrieved_json = retrieve_json_data(json_data_dict, selected_questions_dict)
    for file_name, category_data in retrieved_json.items():
        new_file_name = file_name.replace("1500", "30")
        json_data_points = []
        for category in category_data.keys():
            json_data_points.extend(category_data[category])
        save_json_data(json_data_points, new_file_name)



# load the dataset
data = []
# with open("data\databricks-dolly-15k.jsonl") as f: # original code for windows
with open("../data/databricks-dolly-15k.jsonl") as f:  # modified file paths for MacOS
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

ids = [item['id'] for item in small_subset]

# with open('data\\databricks-dolly-60.json', 'w') as f:
#     json.dump(small_subset, f, default=str, indent=2)

# # add IDs
# csv_path = 'annotation\databricks-dolly-60-name.csv'
# with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
#     fieldnames = [
#         'id', 'length_relevance', 'length_perfomance', 'structure_relevance', 'structure_perfomance',
#         'informativity_relevance', 'informativity_perfomance', 'manner_relevance', 'manner_perfomance',
#         'coherence_relevance', 'coherence_perfomace', 'evidence_relevance', 'evidence_perfomance',
#         'correctness_relevance', 'correctness_perfomance', 'certainty_relevance', 'certainty_perfomance']
#
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#
#     for _id in ids:
#         writer.writerow({'id': _id})

# Calculate the number of items needed for the additional data
additional_data_size = 1500 // len(chosen)  # each person 300
additional_annotation_data = []

# equal number data from each category, if sufficient
for cat in chosen:
    category_items = [item for item in filtered_data if item['category'] == cat and item['id'] not in ids]
    additional_annotation_data.extend(category_items[:additional_data_size])

random.shuffle(additional_annotation_data)

databricks = [additional_annotation_data[i:i + (len(additional_annotation_data) // 5)] for i in range(0, len(additional_annotation_data), len(additional_annotation_data) // 5)]

# saving 300 datapoints for annotation as .json files
# for i, brick in enumerate(databricks):
#     json_name = f'../data/databricks-dolly-1500_part{i + 1}.json'
#     csv_name = f'../annotation/databricks-dolly-1500_part{i + 1}.csv'
#     with open(json_name, 'w') as json_file:
#         json.dump(brick, json_file, default=str, indent=2)
#     write_csv_with_ids(json_name, csv_name)


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
    print("placeholder")

    # # generate csv with ids for model responses with extra usefulness column
    # data_directory = "../data/"
    # files = os.listdir(data_directory)
    # json_files = [file for file in files if file.startswith("llama13bchat_responses_databricks-dolly-30") and file.endswith(".json")]
    # print(json_files)
    # for json_file in json_files:
    #     json_name = data_directory+json_file
    #     csv_name = f'../annotation/'+json_file.replace(".json",".csv")
    #     write_csv_with_ids(json_name, csv_name)

    # # select random data points for model generations
    # select_questions_for_llm_response("../data/", "../annotation/")

    # drop columns for 60 annotations
    # name = "name"
    # # please put your name and run the method
    # # the helper method konly run once remember to back up your file
    # input_file = f'../annotation/databricks-dolly-60-{name}.csv'
    # reduce_components_column(input_file, input_file)


    # for i in range(5):  # check data distribution
    #     file_path = f'../data/databricks-dolly-1500_part{i+1}.json'
    #     print(file_path)
    #     data_length, category_counts = count_categories(file_path)
    #     print(data_length)
    #     print(category_counts)
    # folder_path = 'C:/Users/User/Documents/UNI/WiSe_2023/RL/Project/annotation'
    # modify_csv_files(folder_path)