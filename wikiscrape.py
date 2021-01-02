import requests
from bs4 import BeautifulSoup
BASE_URL = "https://en.wikipedia.org/wiki/"

in_string = input("Enter page name =>").strip()
user_req = "woodstock" if in_string == "" else in_string
res = requests.get(BASE_URL + user_req)

soup = BeautifulSoup(res.content, 'html.parser')
def get_key_from_counters(sections, sub_sections, sub_sub_sections):
    if sub_sub_sections != 0:
        return f"{sections}.{sub_sections}.{sub_sub_sections}"
    elif sub_sections != 0:
        return f"{sections}.{sub_sections}"
    else:
        return f"{sections}"
class_list = []
tags = {tag.name for tag in soup.find_all()} 
content_tag = 0
for tag in tags:  
    for i in soup.find_all( tag ):  
        if i.has_attr( "class" ):  
            if len( i['class'] ) != 0: 
                class_list.append(" ".join(i['class'])) 
            if " ".join(i['class']) == 'mw-parser-output':
                content_tag = i 

stored = {}
section_counter = 0
sub_section_counter = 0
sub_sub_section_counter = 0
title_name = soup.h1.text
stored[title_name] = {}
sec_name = ""
sub_sec_name = ""
sub_sub_sec_name = ""
contents = {}
for sibling in content_tag.findChildren():
    if sibling.name == 'h2':
        section_counter += 1
        sub_section_counter = 0
        contents[str(section_counter)] = sibling.get_text()[:-6]
    elif sibling.name == 'h3':
        sub_section_counter += 1
        sub_sub_section_counter = 0
        contents[f"{section_counter}.{sub_section_counter}"] = sibling.get_text()[:-6]
    elif sibling.name == 'h4':
        sub_sub_section_counter += 1
        contents[f"{section_counter}.{sub_section_counter}.{sub_sub_section_counter}"] = sibling.get_text()[:-6]
    elif sibling.name in ('p', 'ul', 'table', 'ol'):
        key = get_key_from_counters(section_counter, sub_section_counter, sub_sub_section_counter)
        if key in stored[title_name].keys():
            stored[title_name][key].append(sibling.get_text())
        else:
            stored[title_name][key] = [sibling.get_text()]
for key in stored[title_name].keys():
    print(key, end = " ")
choice = 'y'
print()
while choice in ('y', 'Y'):
    for key in contents.keys():
        print(f"{key} {contents[key]}")
    user_key = input("Enter number of the section you want to view => ")
    keys = []
    for key in contents.keys():
        if key.startswith(user_key):
            keys.append(key)
    for key in keys:
        print(key, contents[key])
        if key in stored[title_name]:
            print(" ".join(stored[title_name][key]))
            
    choice = input("Enter y to continue => ")