dbinfo = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "port": 3306,
}

count = 10

val_list =[]
with open("data.txt", "r") as f:
    for i in f:
        if count < 0:
            break
        val_list.append(i.split("\t")[1:-1])
        count -= 1
        
print(val_list)

ins_sql = "INSERT INTO {}(name,location,district,price) VALUES ({}, {},{});"
sql = ins_sql.format('web_neighbourhood','%s','%s','%s')
cursor = dbinfo.cursor()
cursor.executemany(sql,val_list)
db.commit()