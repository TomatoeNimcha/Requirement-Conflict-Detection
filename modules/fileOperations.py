
import os
import json

# Class to handle operation between json files and the requirement table
class FileOperations:
    
    # Method to convert requirement list into dictionary for json import
    def table_to_dictionary(title="",author="",table_contents=[]):
        requirement_list = []

        for _, req_id, req_text, req_att in table_contents:
            if req_id or req_text or req_att:
                requirement_list.append({
                    "requirementID": req_id,
                    "requirement": req_text,
                    "attributes" : req_att
                })

        return {
            "title": title,
            "author": author,
            "requirementList": requirement_list
        }

    # Method toconvert dictionary from json for requirement list
    def dictionary_to_table(data):
        title = data.get("title", "Untitled")
        author = data.get("author", "Unknown")
        requirement_list = data.get("requirementList", [])

        return title, author, requirement_list

    # Method to read chosen file
    def read_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Method to write chosen file
    def write_file(filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # Method to load file into the program, using os path
    def load_file(filename):
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        path = os.path.join(base_dir, "data", filename)

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    # Method to save data into a chosen file, using os path      
    def save_file(filename, data):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)

        path = os.path.join(data_dir, filename)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    # Method to get file path in os
    def get_file_path(foldername, filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        project_root = os.path.abspath(os.path.join(base_dir, ".."))  
        return os.path.join(project_root, foldername, filename)