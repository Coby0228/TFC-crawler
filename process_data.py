import json


input_filename = 'data/raw/TFC_migration_data.json'
output_filename = 'data/dataset/TFC_data_with_labels.json'


with open(input_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"成功讀取檔案 '{input_filename}'，共 {len(data)} 筆資料。")

for item in data:
    if item['verdict'] == '錯誤':
        item['label'] = "False" 
    else:
        item['label'] = 'half'


with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"處理完成！已將結果儲存至 '{output_filename}'。")
