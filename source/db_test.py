import sqlite3

# 连接到数据库（如果不存在则自动创建）
conn = sqlite3.connect('example.db')

# 创建一个游标对象
c = conn.cursor()

# 创建一个包含主键的表，并将表名、列名和列类型更正
c.execute('''
    CREATE TABLE IF NOT EXISTS AA (
        id INTEGER PRIMARY KEY,
        Gas_name TEXT,
        Energy REAL
    )
''')

# 向表中插入测试数据（使用参数化查询）
data = [('methane', 55.5), ('propane', 125.8), ('butane', 138.3),
        ('ethane', 51.9)]
c.executemany("INSERT INTO AA (Gas_name, Energy) VALUES (?, ?)", data)

# 提交更改并关闭连接
conn.commit()
conn.close()
