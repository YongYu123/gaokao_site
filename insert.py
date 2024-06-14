import sqlite3
import tabula


def is_integer(value):
    try:
        int_value = int(value)
        return int_value == value  # Check if the integer conversion is exact
    except (ValueError, TypeError):
        return False


conn = sqlite3.connect('database/college_data.db')
c = conn.cursor()

# 创建示例表
c.execute('''CREATE TABLE admissions
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              major TEXT, 
              school TEXT, 
              quota INTEGER, 
              score INTEGER, 
              rank INTEGER)''')

pdf_path = 'score.pdf'

page_number = 'all'  # Example: '1' for the first page, '2' for the second page, etc.

# Extract tables from the specified page
tables = tabula.read_pdf(pdf_path, pages=page_number,pandas_options={'header': None})

for table in tables:
    # table = table[table[4].apply(lambda x: is_integer(x))]
    for index, row in table.iterrows():
        major,school,quota,rank, score= row[0],row[1],row[2],row[3],row[4]
        c.execute("INSERT INTO admissions (major, school, quota, score, rank) VALUES (?, ?, ?, ?, ?)",(major,school,quota,score,rank))
conn.commit()
conn.close()
