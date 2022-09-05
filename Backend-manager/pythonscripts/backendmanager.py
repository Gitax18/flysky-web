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


# declaring sessions state variables ------------------------------------------------------------------
if "isuserlogin" not in st.session_state.keys():
    st.session_state.isuserlogin = False

if "username" not in st.session_state.keys():
    st.session_state.username = ''

if "password" not in st.session_state.keys():
    st.session_state.password = ''


# defining functions ---------------------------------------------------------------------------------
def loginstatetrue():
    st.session_state.isuserlogin = True

# option menu ----------------------------------------------------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["Home","Login","Flight Data","Passengers Data"],
    icons=["house","person", "",""],
    orientation="horizontal",
    styles={
        "menu-title":{'margin':'0 0 0 45%',"font-size":"25px","font:weight":"900"}
    }
)

if selected == "Home":
    with st.container():
        leftcol,midcol,rightcol = st.columns((1,3,1))
        with leftcol:
            pass
        with midcol:
            st.write("#")
            st.write("#")
            st.markdown("<h1 >Welcome to Flysky <br> Backend Management System </h1>", unsafe_allow_html=True)
            st.write('#')
            st.markdown("<h3>With this application you can visualize flights and airline data and <br> <br> you can update and modify database data and create and book e-tickets.</h3>", unsafe_allow_html=True)


if selected == "Login":
    with st.container():
        st.title("Login")
        st.write("##")
        with st.form("login form", clear_on_submit=True):
            user = st.text_input("username: ")
            pwd = st.text_input("password: ")
            btn = st.form_submit_button("Submit", on_click=loginstatetrue)

            if btn:
                if user != "admin" and pwd != "root":
                    st.warning("please check your details")
                else:
                    st.session_state.isuserlogin = True 
                    st.session_state.username = "Gitanshu"
                    st.success("login succesfully")


if selected == "Passengers Data":
    if st.session_state.isuserlogin:
        st.markdown("<h1 style='font-size:60px'>Welcome {} </h1>".format(st.session_state.username), unsafe_allow_html=True)
        class_data = st.checkbox("show passengers data")
        passenger_data = st.checkbox("show registered users data")
        if class_data:
            st.subheader("Passengers data:")
            qry="select * from passengers"
            _df = pd.read_sql(qry, mydb)
            st.table(_df)
     
        if passenger_data:
            st.subheader("Users data:")
            qry="select * from users"
            _df = pd.read_sql(qry, mydb)
            st.table(_df)
    else:
        st.warning("please login to load data")
                    
if selected == "Flight Data":
    if st.session_state.isuserlogin:
        st.markdown("<h1 style='font-size:60px'>Welcome {} </h1>".format(st.session_state.username), unsafe_allow_html=True)
        st.subheader("Flights data:")
        qry="select airline,class,cost,time from flightdetails"
        _df = pd.read_sql(qry, mydb)
        st.table(_df)
        st.markdown("***")
        st.title("Modify flight class cost and time:")
        airline = st.selectbox("Choose airline:",('None','Indigo','Spicejet'))

        # if choosen airline is indigo
        if airline == 'Indigo':
            fclass = st.selectbox("Choose class:",('None','Economy','Business','Sweet'))
            if fclass == 'Economy':
                st.title("Airline: Indigo")
                st.title("Class: Economy")
                with st.form('modify ind eco data'):
                    cost = st.text_input('Enter new cost: ')
                    time = st.text_input('Enter new time: ')
                    btn = st.form_submit_button('submit')
                    if btn:
                        if cost =='' or time == '':
                            st.warning("please enter details")
                        else:
                            cur.execute("update flightdetails set cost={}, time='{}' where (airline='indigo' and class='Economy')".format(cost,time))
                            mydb.commit()
                            st.success("Done")

            if fclass == 'Business':
                st.title("Airline: Indigo")
                st.title("Class: Business")
                with st.form('modify ind bus data'):
                    cost = st.text_input('Enter new cost: ')
                    time = st.text_input('Enter new time: ')
                    btn = st.form_submit_button('submit')
                    if btn:
                        if cost =='' or time == '':
                            st.warning("please enter details")
                        else:
                            cur.execute("update flightdetails set cost={}, time='{}' where (airline='indigo' and class='Business')".format(cost,time))
                            mydb.commit()
                            st.success("Done")

            if fclass == 'Sweet':
                st.title("Airline: Indigo")
                st.title("Class: Sweet")
                with st.form('modify ind sweet data'):
                    cost = st.text_input('Enter new cost: ')
                    time = st.text_input('Enter new time: ')
                    btn = st.form_submit_button('submit')
                    if btn:
                        if cost =='' or time == '':
                            st.warning("please enter details")
                        else:
                            cur.execute("update flightdetails set cost={}, time='{}' where (airline='indigo' and class='Sweet')".format(cost,time))
                            mydb.commit()
                            st.success("Done")

        # if choosen airline is spicejet
        if airline == 'Spicejet':
            fclass = st.selectbox("Choose class:",('None','Economy','Business','Sweet'))
            if fclass == 'Economy':
                st.title("Airline: Spicejet")
                st.title("Class: Economy")
                with st.form('modify spi eco data'):
                    cost = st.text_input('Enter new cost: ')
                    time = st.text_input('Enter new time: ')
                    btn = st.form_submit_button('submit')
                    if btn:
                        if cost =='' or time == '':
                            st.warning("please enter details")
                        else:
                            cur.execute("update flightdetails set cost={}, time='{}' where (airline='spicejet' and class='Economy')".format(cost,time))
                            mydb.commit()
                            st.success("Done")

            if fclass == 'Business':
                st.title("Airline: Spicejet")
                st.title("Class: Business")
                with st.form('modify spi bus data'):
                    cost = st.text_input('Enter new cost: ')
                    time = st.text_input('Enter new time: ')
                    btn = st.form_submit_button('submit')
                    if btn:
                        if cost =='' or time == '':
                            st.warning("please enter details")
                        else:
                            cur.execute("update flightdetails set cost={}, time='{}' where (airline='spicejet' and class='Business')".format(cost,time))
                            mydb.commit()
                            st.success("Done")

            if fclass == 'Sweet':
                st.title("Airline: Spicejet")
                st.title("Class: Sweet")
                with st.form('modify spi sweet data'):
                    cost = st.text_input('Enter new cost: ')
                    time = st.text_input('Enter new time: ')
                    btn = st.form_submit_button('submit')
                    if btn:
                        if cost =='' or time == '':
                            st.warning("please enter details")
                        else:
                            cur.execute("update flightdetails set cost={}, time='{}' where (airline='spicejet' and class='Sweet')".format(cost,time))
                            mydb.commit()
                            st.success("Done")



    else:
        st.warning("please login to load data")