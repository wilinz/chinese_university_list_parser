import pandas as pd
import requests

# URL of the Excel file
excel_url = 'http://www.moe.gov.cn/jyb_xxgk/s5743/s5744/A03/202110/W020211027623974108131.xls'
headers = {
    'Referer': 'http://www.moe.gov.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}
# Send a HTTP request to the URL and get the content
response = requests.get(excel_url, headers=headers)
assert response.status_code == 200, f"Failed to download the file: {response.status_code}"

# Save the content to a temporary file
with open('temp_file.xls', 'wb') as file:
    file.write(response.content)

# Read the Excel file using pandas, with dtype specified for '学校标识码'
dtype_spec = {'学校标识码': str}
df = pd.read_excel('temp_file.xls', header=2, dtype=dtype_spec)

# Filter out rows where the '学校标识码' column is empty
filtered_df = df[df['学校标识码'].notna()]

column_mapping = {
    '序号': 'id',
    '学校名称': 'name',
    '学校标识码': 'code',
    '主管部门': 'manager',
    '所在地': 'city',
    '办学层次': 'level',
    '备注': 'remarks'
}

# Rename the columns using the mapping dictionary
filtered_df = filtered_df.rename(columns=column_mapping)

# Convert the filtered and renamed DataFrame to JSON
json_data = filtered_df.to_json(orient='records', force_ascii=False,indent=4)

# Save the JSON data to a file
with open('universities.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print("Filtered and renamed Excel file has been converted to JSON and saved as 'universities.json'")