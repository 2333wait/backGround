import json
import pymysql
import csv
# 定义 MySQL 数据库连接参数
db_host = "localhost"
db_name = "china2023"
db_user = "root"
db_password = "123456"

# 创建数据库连接
conn = pymysql.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

def dict_pairs(pairs):
    d = {}
    for k, v in pairs:
        d[k] = v
    return d

# 打开 JSON 文件并将其解析为 Python 字典
with open("D:\BaiduNetdiskDownload\json1.json", "r") as f:
    lines = f.readlines()

print(lines[0])
header = list(lines[0].keys())
with open('file.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    for row in lines:
        writer.writerow(row)


