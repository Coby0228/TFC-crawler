import json
import re


input_filename = 'data/raw/TFC_migration_data.json'
output_filename = 'data/dataset/TFC_data_with_labels.json'


def map_function(verdict):
    """
    Maps the verdict to a label ('false' or 'half').
    """
    if verdict in ['錯誤', '詐騙', '移花接木', '假借冠名', '影像變造', '影音變造']:
        return 'false'
    else:
        return 'half'


with open(input_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, list):
    for item in data:
        if 'verdict' in item and item['verdict']:
            item['label'] = map_function(item['verdict'])
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
