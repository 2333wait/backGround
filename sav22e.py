import json
import pymysql

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

with open("D:\BaiduNetdiskDownload\json1.json", "r") as f:
    data = json.load(f)
cursor = conn.cursor()
values = []
for record in data:
    cursor = conn.cursor()
    print(record["id"])
    print("ddddd")
    values.append((record["id"], record["seq"], record["is_moving"],record["position"], record["shape"], record["orientation"],record["velocity"], record["type"], record["heading"],record["time_meas"], record["ms_no"]))
cursor.execute(
    """
    INSERT INTO your_table (id, seq, is_moving, position, shape, orientation,velocity, type, heading,time_meas, ms_no)
    VALUES (%d,%d,%d,%s, %s, %d,%d,%d,%d,%d,%d);
    """,
    values
    #(record["id"], record["seq"], record["is_moving"],record["position"], record["shape"], record["orientation"],record["velocity"], record["type"], record["heading"],record["time_meas"], record["ms_no"])
)
conn.commit()

# 关闭数据库连接
conn.close()


