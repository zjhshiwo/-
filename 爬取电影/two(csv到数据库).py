import csv
import pymysql

def readData():
    result=[]
    with open('D:/cs.csv','r',encoding='UTF-8') as csvfile:
        csv_reader=csv.reader(csvfile)
        for row in csv_reader:
            for a in row:
                result.append(a)
    return result


db=pymysql.connect("localhost","root","123456","mysql")
cursor=db.cursor()
res=readData()
print(res)
sql="INSERT INTO testmodel_test(Name) VALUES(%s)"
for a in res:
    cursor.execute(sql,(a))
    db.commit()
db.close()