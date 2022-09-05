# from asyncio import SafeChildWatcher
from turtle import onclick
import streamlit as st
from PIL import Image as im
from streamlit_option_menu import option_menu
import mysql.connector as ms
from fpdf import FPDF 

# all variables used in program
login_state = None
loggedin_users = []
loggedin_users_password = []
users_islogging = []
global airline
airline = None

# initializing sesstion state keys
if "username" not in st.session_state.keys():
    st.session_state.username = "root"

if "password" not in st.session_state.keys():
    st.session_state.password = 1

if "from" not in st.session_state.keys():
    st.session_state['from'] = "a"

if "to" not in st.session_state.keys():
    st.session_state['to'] = "b"

if "class" not in st.session_state.keys():
    st.session_state['class'] = "c"

if "date" not in st.session_state.keys():
    st.session_state['date'] = "d"

if "indtime" not in st.session_state.keys():
    st.session_state['indtime'] = ""

if "indcost" not in st.session_state.keys():
    st.session_state['indcost'] = ""

if "spitime" not in st.session_state.keys():
    st.session_state['spitime'] = ""

if "spicost" not in st.session_state.keys():
    st.session_state['spicost'] = ""

if "showpassform" not in st.session_state.keys():
    st.session_state.showpassform = False

if "showindpay" not in st.session_state.keys():
    st.session_state.showindpay = False

if "indpaydone" not in st.session_state.keys():
    st.session_state.indpaydone = False

if "showspipay" not in st.session_state.keys():
    st.session_state.showspipay = False

if "spipaydone" not in st.session_state.keys():
    st.session_state.spipaydone = False




# making connection to databse
mydb = ms.connect(
    host="localhost",
    user="root",
    password="",
    database="airline"
)
# making the cursor to execute the db commands
cur = mydb.cursor()

# getting list of users and their passwords  who have logged in 
cur.execute('select username from users order by id')
for i in cur:
    for j in i:
        loggedin_users.append(j)

cur.execute('select password from users order by id')
for i in cur:
    for j in i:
        loggedin_users_password.append(j)

cur.execute('select isloggin from users')
for i in cur:
    for j in i:
        users_islogging.append(j)



# setting up page content
st.set_page_config(
    page_title="Flysky",
    page_icon=":airplane:",
    layout="wide",
    
)


# making the navbar 
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=['Home', 'Login', 'Register'],
        icons=['house', 'person', 'person-circle'],
        default_index=0
        # orientation="horizontal"
    )

def createticket(airline, name, fromdest, todest, date, time, fclass,filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.image("images/{}.png".format(airline), 10, 10, 50)
    pdf.set_font("ARIAL",'B', 23)
    pdf.text(10,50, txt='FROM: {}'.format(fromdest))
    pdf.text(100, 50, txt='TO: {}'.format(todest))
    pdf.set_font('ARIAL','',15)
    pdf.text(10, 600, txt='{}'.format(name))
    pdf.text(10,70,txt='Date: {}'.format(date))
    pdf.text(60,70, txt='Time: {}'.format(time))
    pdf.text(110,70, txt='Class: {}'.format(fclass))
    pdf.image('images/barcode.png', 5, 75, 60)
    return pdf.output('passengerstickets/'+filename+'.pdf')



# making login page content
if selected == "Login":
    with st.container():
        left, mid, right = st.columns((2,3,2))
    with mid:
        with st.form("loginform", clear_on_submit=True) :
            user_name = st.text_input("username: ")
            pass_word = st.text_input("password: ")
            login_button = st.form_submit_button(label="submit")
            if login_button == True:
                if user_name == "" or pass_word == "":
                    st.warning("please enter valid details")
                if user_name not in loggedin_users:
                    st.warning("username does not exist please make an account")
                if user_name in loggedin_users:
                    # store data in database
                    if pass_word not in loggedin_users_password:
                        st.warning("password not in list")
                    elif loggedin_users.index(user_name) == loggedin_users_password.index(pass_word):
                        st.session_state['username'] = user_name
                        st.session_state['password'] = pass_word
                        st.session_state['login_state'] = "true"
                        st.success("logged in")
                        if users_islogging[loggedin_users.index(user_name)] == "false":
                            cur.execute("UPDATE users SET isloggin = 'true' where username = '{}' ".format(user_name))
                            mydb.commit()
                                

# making home page content
if selected == "Home":
    # code for home page
    # to show content after chossing destinartion
    if "showfurcont" not in st.session_state.keys():
        st.session_state.showfurcont = False
    
    # main content
    with st.container():
        leftcol, rightcol = st.columns(2)
        with leftcol:
             #code fot  left column content
            st.write("---")
            st.write("###")
            st.title("Welcome to FlySky Travels,")
            st.subheader(" Get best domestics and international")
            st.subheader("flights at best prices")
        with rightcol:
            # code for right column content
            st.write("---")
            st.write("###")
            with st.form("myform", clear_on_submit=True):
                From = st.text_input("From: ").capitalize()
                To = st.text_input("To: ").capitalize()
                flight_class = st.selectbox(
                'Select class:',
                ('Economy', 'Business', 'Sweet'))
                Date = st.date_input(label="Select date: ")

                button_value = st.form_submit_button(label="submit")

                if(button_value==True):
                    try:
                        if From == "" or To == "":
                           st.warning("please enter your destinations.")

                        else:
                            if st.session_state.username == '':
                                st.warning("please login to continue")
                            else:
                                st.session_state.showfurcont = True   
                                
                                st.session_state['from'] = From 
                                st.session_state['to'] = To
                                st.session_state['class'] = flight_class 
                                st.session_state['date'] = Date 
                    except:
                        st.warning("please login")
        #  content to be show when user get logged in and choosec his/her destination
        with st.container():
            if button_value == True or st.session_state.showfurcont == True:
                st.session_state.showfurcont = True
                st.title("Available Flights")
                indleft,indmid,indright = st.columns((2,4,2)) #indigo columns
                spileft,spimid,spiright = st.columns((2,4,2)) #spicejet columns
                st.write("##")
                #################### indigo
                with indleft:
                    st.image(im.open('images/indigo.png'), width=230)                    
                    st.write("---")

                with indmid:
                    st.markdown('''    <h2>From:  {} </h2>
                    <h2>To:  {} </h2>
                     '''.format(st.session_state['from'].capitalize(),st.session_state['to'].capitalize()), unsafe_allow_html=True)
                    st.write("---")

                with indright:
                    cur.execute('select time from flightDetails where airline= "indigo" && class="{}"'.format(st.session_state['class']) )
                    for i in cur:
                        for k in i:
                            st.session_state['indtime'] = k
                    cur.execute('select cost from flightDetails where airline= "indigo" && class="{}"'.format(st.session_state['class']) )
                    for i in cur:
                        for k in i:
                            st.session_state['indcost'] = k
                    st.subheader("Time: "+st.session_state['indtime'])
                    st.subheader("₹"+str(st.session_state['indcost']))
                    st.write("---")

                    ################### spicejet
                with spileft:
                    st.image(im.open('images/spicejet.png'), width=230)
                    st.write("---")

                with spimid:
                    st.markdown('''    <h2>From:  {} </h2>
                    <h2>To:  {} </h2>
                     '''.format(st.session_state['from'].capitalize(),st.session_state['to'].capitalize()), unsafe_allow_html=True)
                    st.write("---")

                with spiright:
                    cur.execute('select time from flightDetails where airline= "spicejet" && class="{}"'.format(st.session_state['class']) )
                    for i in cur:
                        for k in i:
                            st.session_state['spitime'] = k
                    cur.execute('select cost from flightDetails where airline= "spicejet" && class="{}"'.format(st.session_state['class']) )
                    for i in cur:
                        for k in i:
                            st.session_state['spicost'] = k
                    st.subheader("Time: "+st.session_state['spitime'])
                    st.subheader("₹"+str(st.session_state['spicost']))
                    st.write("---")

                def showpassform():
                    st.session_state.showpassform = True

                airline = st.button("select airline", on_click=showpassform)

    with st.container():
        if airline or st.session_state.showpassform:
            st.subheader("Select airline from above available flights ")
            st.session_state.showpassform = True
            airlineopt = st.selectbox("",('none','indigo','spicejet'))

# indigo form
            if airlineopt == "indigo":
                st.subheader("enter passenger details:".capitalize())
                leftcol, rightcol = st.columns((5,2))
                with leftcol:

                    with st.form("indigo passenger form"):
                        passfirstname = st.text_input("Firstname: ")
                        passlastname = st.text_input("Lastname: ")
                        passadharno = st.text_input("Aadhar No. : ")
                        passemail = st.text_input("Email: ")
                        passgender = st.selectbox('Select gender',('male','female'))
                        if passgender == 'male':
                            name = 'Mr. '+passfirstname+' '+passlastname
                        elif passgender == "female":
                            name = 'Ms. '+passfirstname+' '+passlastname

                        def showindpay():
                            st.session_state.showindpay = True

                        submitpassform = st.form_submit_button("submit", on_click=showindpay)

                        if submitpassform:
                            if passfirstname == '' or passlastname == ''  or passemail == '':
                                st.warning("please fill all detalis")
                            else:
                                st.session_state.showindpay = True
                                qry = '''
                                INSERT INTO passengers(firstname, lastname, aadharno, email, time, class, date, fromdest, todest, username )
                                VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")
                                '''.format(passfirstname,passlastname,passadharno, passemail,st.session_state['indtime'],st.session_state['class'],st.session_state['date'],st.session_state['from'],st.session_state['to'], st.session_state['username'] )
                                
                                cur.execute(qry)
                                mydb.commit()


                with rightcol:
                    st.image(im.open('images/indigo.png'),width=250)
                    st.subheader('From: '+st.session_state['from'])
                    st.subheader('To: ' +st.session_state['to'])
                    st.subheader('cost: ' +'₹'+str(st.session_state['indcost']))
                
                if st.session_state.showindpay == True:
                    st.title("Make payment:")
                    payopt = st.selectbox("choose payment option",("None","Credit", "Debit"))
                    if payopt == "Credit":
                        with st.form("indigo credit payment"):
                            st.radio("select card type:",('VISA', 'MASTERCARD'))
                            st.text_input("Card number: ")
                            st.text_input("Email: ")
                            st.text_input("Mobile number")
                            def paydone():
                                st.session_state.indpaydone == True
                            paybtn = st.form_submit_button("Proceed", on_click=paydone)
                            if paybtn or st.session_state.indpaydone == True:
                                cur.execute("update passengers set makepayment = 'true' where aadharno = '{}' and date = '{}'". format(passadharno, st.session_state['date']))
                                mydb.commit()
                                cur.execute("select * from passengers where aadharno = '{}' and date = '{}'". format(passadharno, st.session_state['date']))
                                titleft,titmid,titright = st.columns((5,3,5))
                                with titleft:
                                    pass
                                with titmid:
                                    # st.title("PAYMENT DONE")
                                    st.image(im.open('images/tick.png'), caption="PAYMENT DONE" ,width=300)
                                    st.balloons()
                                with titright: 
                                    pass
                            
                        if paybtn or st.session_state.indpaydone == True:
                            st.title("Download ticket")
                            createticket("indigo",name,st.session_state['from'],st.session_state['to'], st.session_state['date'], st.session_state['indtime'],st.session_state['class'],passadharno+passfirstname)
                            ticket = 'passengerstickets/'+passadharno+passfirstname+'.pdf'
                            with open(ticket,'rb') as file:
                                pdfbytes = file.read()

                            st.download_button("Download ticket",data=pdfbytes,file_name=ticket, mime='application/octet-stream')

# spicejet form
            elif airlineopt == "spicejet":
                st.subheader("enter passenger details:".capitalize())
                leftcol, rightcol = st.columns((5,2))
                with leftcol:

                    with st.form("spicejet passenger form", clear_on_submit=True):
                        passfirstname = st.text_input("Firstname: ")
                        passlastname = st.text_input("Lastname: ")
                        passadharno = st.text_input("Aadhar No. : ")
                        passemail = st.text_input("Email: ")
                        passgender = st.selectbox('Select gender',('male','female'))
                        if passgender == 'male':
                            name = 'Mr. '+passfirstname+' '+passlastname
                        elif passgender == "female":
                            name = 'Ms. '+passfirstname+' '+passlastname

                        submitpassform = st.form_submit_button("submit")

                        if submitpassform:
                            if passfirstname == '' or passlastname == ''  or passemail == '':
                                st.warning("please fill all detalis")
                            else:
                                st.session_state.showspipay = True
                                qry = '''
                                INSERT INTO passengers(firstname, lastname, aadharno, email, time, class, date, fromdest, todest, username )
                                VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")
                                '''.format(passfirstname,passlastname,passadharno, passemail,st.session_state['spitime'],st.session_state['class'],st.session_state['date'],st.session_state['from'],st.session_state['to'], st.session_state['username'] )
                                
                                cur.execute(qry)
                                mydb.commit()
                with rightcol:
                    st.image(im.open('images/spicejet.png'),width=250)
                    st.subheader('From: '+st.session_state['from'])
                    st.subheader('To: ' +st.session_state['to'])
                    st.subheader('cost: ' +'₹'+str(st.session_state['spicost']))

                if st.session_state.showspipay == True:
                    st.title("Make payment:")
                    payopt = st.selectbox("choose payment option",("None","Credit", "Debit"))
                    if payopt == "Credit":
                        with st.form("spicejet payment"):
                            st.radio("select card type:",('VISA', 'MASTERCARD'))
                            st.text_input("Card number: ")
                            st.text_input("Email: ")
                            st.text_input("Mobile number")
                            def spipaydone():
                                st.session_state.spipaydone == True
                            sppaybtn = st.form_submit_button("Proceed", on_click=spipaydone)
                            if sppaybtn or st.session_state.spipaydone == True:
                                cur.execute("update passengers set makepayment = 'true' where aadharno = '{}' and date = '{}'". format(passadharno, st.session_state['date']))
                                mydb.commit()
                                cur.execute("select * from passengers where aadharno = '{}' and date = '{}'". format(passadharno, st.session_state['date']))
                                titleft,titmid,titright = st.columns((5,3,5))
                                with titleft:
                                    pass
                                with titmid:
                                    # st.title("PAYMENT DONE")
                                    st.image(im.open('images/tick.png'), caption="PAYMENT DONE" ,width=300)
                                    st.balloons()
                                with titright: 
                                    pass
                            
                        if sppaybtn or st.session_state.spipaydone == True:
                            st.title("Download ticket")
                            createticket("spicejet",name,st.session_state['from'],st.session_state['to'], st.session_state['date'], st.session_state['spitime'],st.session_state['class'],passadharno+passfirstname)
                            ticket = 'passengerstickets/'+passadharno+passfirstname+'.pdf'
                            with open(ticket,'rb') as file:
                                pdfbytes = file.read()

                            btn = st.download_button("Download ticket",data=pdfbytes,file_name=ticket, mime='application/octet-stream')
                            if btn:
                                st.session_state.showpassform = False
                                st.session_state.showindpay = False
                                st.session_state.indpaydone = False
                                st.session_state.showspipay = False
                                st.session_state.spipaydone = False




                                

                
if selected == "Register":
    st.title("Make an account")
    with st.form("registerform", clear_on_submit=True):
        username = st.text_input("username: ")
        firstname = st.text_input("firstname: ")
        lastname = st.text_input("lastname: ")
        email = st.text_input("email: ")
        password = st.text_input("password: ")

        register_button = st.form_submit_button(label="submit")

        if register_button == True:
            if username in loggedin_users:
                st.warning("username already exist")
            else:
                cur.execute('''
                INSERT INTO users(username, firstname, lastname, email, password) 
                VALUES('{}','{}','{}','{}','{}')
                '''.format(username, firstname, lastname, email, password))
                mydb.commit()
                st.success("account created now you can log in to your account from login page")
