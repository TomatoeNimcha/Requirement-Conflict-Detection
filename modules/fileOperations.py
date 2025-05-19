
import os
import json

class FileOperations:
    
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

    def dictionary_to_table(data):
        title = data.get("title", "Untitled")
        author = data.get("author", "Unknown")
        requirement_list = data.get("requirementList", [])

        return title, author, requirement_list

    def read_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_file(filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_file(filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Current file directory
        template_path = os.path.join(base_dir, "data", "template", filename)

        with open(template_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data