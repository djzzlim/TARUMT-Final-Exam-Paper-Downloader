import requests
import json
import re
import os

print("""
********************************************
* TARUMT Final Exam Paper Downloader       *
*                                          *
* Automatically download final exam papers *
* from Tunku Abdul Rahman University's     *
* Vlib.                                    *
*                                          *
********************************************
""")

url = 'http://eprints.tarc.edu.my/cgi/search/archive/simple/export_inhousedb_JSON.js'

user = input("\nUsername: ")
passwd = input("Password: ")

while True:
    print("Type 'Exit' or '' to QUIT")
    subject_code = input("Please enter Subject Code: ")

    if subject_code == "" or subject_code.lower() == 'exit':
        break

    params = {
        'screen': 'Search',
        'dataset': 'archive',
        '_action_export': '1',
        'output': 'JSON',
        'exp': f'0|1|-date/creators_name/title|archive|-|q:abstract/creators_name/date/documents/title:ALL:IN:{subject_code}|-|eprint_status:eprint_status:ANY:EQ:archive|metadata_visibility:metadata_visibility:ANY:EQ:show'
    }

    response = requests.get(url, params=params)

    data = response.text
    data = data.replace("'", '"')
    parsed_data = json.loads(data)

    document_uris = []
    file_links = []
    titleid = ""

    for document in parsed_data:
        titleid = document.get("title", "")
        uri = document.get("uri")
        document_uris.append(document["documents"])

    for items in document_uris:
        for item in items:
            if (item["mime_type"] == 'application/pdf'):
                file_links.append(item["uri"])

    titleid = re.sub(r'\s*\(.*?\)', '', titleid)
    print("\n" + titleid)

    # Create "Final Exam" directory if it doesn't exist
    if not os.path.exists('Final Exam'):
        os.mkdir('Final Exam')

    # Create subdirectory for the titleid
    titleid_path = os.path.join('Final Exam', titleid)
    if not os.path.exists(titleid_path):
        os.mkdir(titleid_path)

    # Download the files to the respective subdirectory
    for i in range(0, len(file_links)):
        print(file_links[i])
        output_path = os.path.join(titleid_path, f'{titleid}-{i+1}.pdf')
        os.system(f"curl -L -X GET {file_links[i]} -i -u {user}:{passwd} -o '{output_path}'")
