import ollama
from data_manager import load_json_data, save_json_data

json_directory = "../data/"
json_data_dict = load_json_data(json_directory, "databricks-dolly-30_")

for file in json_data_dict.keys():
    print("File: ", file)
    generated_responses = []
    for json_data in json_data_dict[file]:
        question = json_data["instruction"]
        context = json_data["context"]
        prompt = f"""Answer the question:\n{question}\nBased on context:\n{context}"""
        response = ollama.chat(model='llama2:13b-chat', messages=[
            {
                'role': 'user',
                'content': prompt,
            'stream': False,
            },
        ])
        print(prompt + "\n")
        print(f"Answer: {response['message']['content']}\n")
        generated_response = response['message']['content']
        json_data["generated_response"] = generated_response
        generated_responses.append(json_data)
        save_json_data(generated_responses, json_directory + "Ollama_responses_" + file)
