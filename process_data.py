import json
import re


input_filename = 'data/raw/TFC_migration_data.json'
output_filename = 'data/dataset/TFC_data_with_labels.json'


with open(input_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, list):
    for item in data:
        if 'verdict' in item:
            if item['verdict'] == '錯誤':
                item['label'] = 'false'
            else:
                item['label'] = 'half'
        else:
            item['label'] = 'half'
        
        if 'url' in item and isinstance(item['url'], str):
            match = re.search(r'migration-(\d+)', item['url'])
            if match:
                item['event_id'] = match.group(1)
            else:
                item['event_id'] = None
        else:
            item['event_id'] = None


with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"處理完成！已將結果儲存至 '{output_filename}'。")
