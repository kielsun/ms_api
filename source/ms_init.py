import sqlite3
import MS_api as ms
import os


def mk_db(db_path, gas_date_dir="../date/VOC_outmol"):
    conn = sqlite3.connect(db_path)
    print('数据库打开成功').__init__()
    c = conn.cursor()  # 创建一个游标对象，用于执行 SQLite 语句
    c.execute('''
    CREATE TABLE IF NOT EXISTS Demol3_gas (
        id INTEGER PRIMARY KEY,
        Gas_name TEXT,
        Energy REAL
    )
    ''')
    for file in os.listdir(gas_date_dir):
        filepath = gas_date_dir + "/" + file
        if not os.path.isdir(filepath):
            date = ms.get_date(filepath)
            infos = ms.get_infos(file)
            res = ms.opt_eg(date)
            gas_name = infos[0]
            c.execute(
                "INSERT OR REPLACE INTO Demol3_gas (Gas_name, Energy) VALUES (?, ?)",
                (gas_name, res))
            #  INSERT OR REPLACE 语句将数据插入到表中，如果 name 列的值已经存在，
            # 则自动更新该行的数据，否则插入新行。这样，就避免了使用 SELECT 语句进行重名检查的过程，从而提高了效率。
    conn.commit()  # 提交更改
    conn.close()
    print("数据库初始化成功!")


if __name__ == "__main__":
    mk_db(r"../date/ms_date.db")
