from openai import OpenAI
client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")

file_list = client.files.list()
 
client.files.delete(file_id="d4i77namisdua6ni63k0eb")
for file in file_list.data:
    print(file) # 查看每个文件的信息