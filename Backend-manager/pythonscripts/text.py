from optparse import Values
import streamlit as st
import pandas as pd
import mysql.connector as ms
from streamlit_option_menu import option_menu

# setting up page content
st.set_page_config(
    page_title="Flysky Manager",
    page_icon=":document:",
    layout="wide",
    
)


# making connection to database
mydb = ms.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'airline'
)
# setting up cursor
cur = mydb.cursor()


values=[]
qry="select count(*) from passengers where class='Economy'"

cur.execute(qry)
for i in cur:
    for k in i:
        values.append(k)

qry="select count(*) from passengers where class='Business'"

cur.execute(qry)
for i in cur:
    for k in i:
        values.append(k)

qry="select count(*) from passengers where class='Sweet'"

cur.execute(qry)
for i in cur:
    for k in i:
        values.append(k)

label = ['Economy','Business','Sweet']
st.write(label)
st.write(values)
dic = {'NAME':label,'values':values}
df = pd.DataFrame(data=dic)
# df.plot.pie(y=values, labels=label)
st.bar_chart(df)