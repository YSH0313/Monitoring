import time
import pymysql

# while True:
#     time.sleep(1)
#     time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
#     if time_now == "00:00:00":  # 此处设置每天定时的时间
# db = pymysql.connect(host='127.0.0.1', user='root', password='root', port=3306, db='django', charset="utf8", use_unicode=True)
db = pymysql.connect(host='117.50.3.204', user='lym', password='Elements123', port=3306, db="adjudicative", charset="utf8", use_unicode=True)
cursor = db.cursor()
select_reg = """SELECT `table_name`,`table_dimensions` FROM moniter_registered"""
cursor.execute(select_reg)
db.commit()
all_reg = cursor.fetchall()
for i in all_reg:
    table_name = i[0]
    table_dimensions = i[1]
    try:
        sql = """SELECT COUNT(id) FROM {table_name}""".format(table_name=table_name)
        cursor.execute(sql)
        db.commit()
    except:
        sql = """SELECT COUNT(kid) FROM {table_name}""".format(table_name=table_name)
        cursor.execute(sql)
        db.commit()
    now_count = cursor.fetchone()[0]
    print(now_count)
    insert_sql = """INSERT INTO `moniter_data_count`(`count`, `dimensions`, `time_date`) VALUES ('{count}', '{dimensions}', '{time_date}');""".format(count=now_count, dimensions=table_dimensions, time_date=str(time.strftime("%Y-%m-%d", time.localtime())))
    cursor.execute(insert_sql)
    db.commit()
db.close()
    #     time.sleep(2)
    # else:
    #     continue