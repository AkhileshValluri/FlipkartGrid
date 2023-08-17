import json

def extract_post_text_content(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'post_text_content':
                yield value
            elif isinstance(value, (dict, list)):
                yield from extract_post_text_content(value)
    elif isinstance(data, list):
        for item in data:
            yield from extract_post_text_content(item)

with open('blog_scrape.json', 'r', encoding='utf-8') as json_file:
    original_data = json.load(json_file)

post_text_contents = list(extract_post_text_content(original_data))

new_data = {
    "post_text_contents":post_text_contents
}

with open('output.json','w') as new_json_file:
    json.dump(new_data,new_json_file,indent=4)

