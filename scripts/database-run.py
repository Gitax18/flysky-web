import mysql.connector as ms

mydb = ms.connect(
    host="localhost",
    user="root",
    password=""
)

cur = mydb.cursor()

cur.execute("DROP DATABASE IF EXISTS airline")

cur.execute('CREATE DATABASE airline')
mydb.commit()

cur.execute('use airline')

cur.execute('''
    CREATE TABLE users(id int auto_increment,
    username varchar(25) unique,
    firstname varchar(25),
    lastname varchar(25),
    email varchar(50),
    password varchar(25),
    isloggin varchar(5) default "false",
    primary key(id) )
''')

mydb.commit()

cur.execute("desc users")

for i in cur:
    print(i)

cur.execute('''
    INSERT INTO users(username, firstname, lastname, email, password) 
    VALUES("git@123", "gitanshu", "sankhla", "gitanshu123@email.com", "git123"),
    ("tanaypro", "tanay", "sankhla", "tanay2345@email.com", "tanay123"),
    ("root","rootfirst","rootlast","root@local.com","1")
''')

mydb.commit()

cur.execute("select * from users")
for k in cur:
    print(k)



cur.execute('''
    CREATE TABLE flightDetails(id int auto_increment,
    airline varchar(25),
    class varchar(25),
    cost int,
    time varchar(25),
    primary key(id))
''')
mydb.commit()

cur.execute("desc flightDetails")

for i in cur:
    print(i)

cur.execute('''
    INSERT INTO flightDetails(airline, class, cost, time) 
    VALUES("indigo", "Economy", 4800, '12:30:00'),
    ("indigo", "Business", 9000, '15:15:00'),
    ("indigo", "Sweet", 20000, '02:00:00'),
    ("spicejet", "Economy", 6700, '18:45:00'),
    ("spicejet", "Business", 14000, '22:50:00'),
    ("spicejet", "Sweet", 28000, '05:15:00')
''')

mydb.commit()

# creating table to store passenger data

cur.execute('''
CREATE TABLE passengers(id int auto_increment,
firstname varchar(25),
lastname varchar(25),
aadharno varchar(15) unique,
email varchar(25),
time varchar(25),
class varchar(25),
date varchar(25),
fromdest varchar(25),
todest varchar(25),
airline varchar(25),
username varchar(25),
makepayment varchar(25) default 'false',  
primary key(id));
''')

mydb.commit()
print("@"*50)

cur.execute('desc passengers')

for i in cur:
    print(i)


input()