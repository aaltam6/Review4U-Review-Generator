#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect
from wtforms import Form,StringField,SubmitField, SelectField
from wtforms.validators import InputRequired,DataRequired
import smtplib
from email.message import EmailMessage
import openai
import os
import mysql.connector

app = Flask(__name__)

openai.api_key = os.getenv('gpt_api')
app.secret_key = os.getenv('app_key')
email_password = os.getenv('email_api')

#class ManagerForm(Form):
    #define two classes for manager and customer to seperate required validators.
    #location = SelectField('Select Field', validators=[DataRequired()], validate_choice=False,choices=[])
    #customer = StringField('customer', validators=[InputRequired()])
    #manager = SelectField('Select Field', validators=[DataRequired()], validate_choice=False,choices=[])
    #email = StringField('email', validators=[InputRequired()])
    #order = SelectField('Select Field', validators=[DataRequired()], validate_choice=False,choices=[])
    #descriptor = StringField('descriptor', validators=[InputRequired()])

class CustomerForm(Form):
    #define two classes for manager and customer to seperate required validators.
    location = StringField('location', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    order = StringField('order', validators=[InputRequired()])
    descriptor = StringField('descriptor', validators=[InputRequired()])

class HomeForm(Form):
    user = StringField('user', validators=[InputRequired()])
    password = StringField('password', validators=[InputRequired()])

class MyForm(Form):
    action1 = SubmitField('Customer')
    action2 = SubmitField('Manager')

#cnx = mysql.connector.connect(user=os.getenv('RDS_USERNAME'), password=os.getenv('RDS_PASSWORD'),
                      #host=os.getenv('RDS_HOSTNAME'),
                      #database=os.getenv('RDS_DB_NAME'))

#cursor = cnx.cursor()

#cursor.execute('SELECT managerID,pass FROM managers')
#result_set = cursor.fetchall()

#cursor.execute('SELECT itemID FROM item')
#results = cursor.fetchall()

#options = [(str(result[0]), str(result[0])) for result in results]

#ManagerForm.order.choices = options


#cursor.execute('SELECT managerName FROM managers')
#resultmanagers = cursor.fetchall()

#optionmanager = [(str(result[0]), str(result[0])) for result in resultmanagers]

#ManagerForm.manager.choices = optionmanager

#cursor.execute('SELECT locationID FROM locations')
#esultlocations = cursor.fetchall()

#optionlocation = [(str(result[0]), str(result[0])) for result in resultlocations]

#ManagerForm.location.choices = optionmanager


#cursor.close()
#cnx.close()

#def writer(location,descriptor,email,customer,reservation,order,response):
    #cnx = mysql.connector.connect(user=os.getenv('RDS_USERNAME'), password=os.getenv('RDS_PASSWORD'),
                      #host=os.getenv('RDS_HOSTNAME'),
                      #database=os.getenv('RDS_DB_NAME'))

    #cursor = cnx.cursor()
    #mealExperience =("INSERT INTO mealExperience(orderID,keyWords,locationID,itemID) VALUES (%(x)s,%(y)s,%(z)s,%(p)s)")
    #values = {'x':reservation,'y':descriptor,'z':location,'p':order}
    #cursor.execute(mealExperience,values)

    #reviewGenerated =("INSERT INTO reviewGenerated(customerID,locationID,review,orderID) VALUES (%(x)s,%(y)s,%(z)s,%(k)s)")
    #values = {'x':email,'y':location,'z':response,'k':reservation}
   #cursor.execute(reviewGenerated,values)

    #cursor.execute('SELECT customerID FROM customer')
    #customer_set = cursor.fetchall()

    #customer_ids = [x[0] for x in customer_set]
    #if email not in customer_ids:
        #customerEntry =("INSERT INTO customer(customerID,fullName) VALUES (%(x)s,%(y)s)")
        #values = {'x':email,'y':customer}
        #cursor.execute(customerEntry,values)
    #else:
        #pass

    #cnx.commit()
    #cursor.close()
    #cnx.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    #include locations.html and login and wrote locations.
    form = MyForm()
    if request.method == 'POST':
        if request.form.get('action1') == 'Customer':
            return redirect(url_for('customer'))
        elif  request.form.get('action2') == 'Manager':
            return redirect(url_for('validator'))
        else:
            return render_template('home.html',form=form)
    else:
            return render_template('home.html',form=form)

@app.route('/validator', methods=['GET', 'POST'])
def validator():
    form = HomeForm(request.form)

    if request.method == 'POST':

        username = 'user'
        password = 'pass'
        result_set = username,password

        if form.validate():
            for x,y in result_set:
                if x == username and y == password:
                    return redirect(url_for('manager'))

                else:
                    return render_template('validator.html',form=form)

        else:
            return render_template('validator.html',form=form)

    else:
        return render_template('validator.html',form=form)



@app.route("/about", methods=['GET', 'POST'])
def about():
    #add words and shit
    if request.method == 'GET':
        return render_template('about.html')


@app.route('/generator/<location>/<descriptor>/<email>/<customer>/<reservation>/<order>/<route>/<manager>/', methods=['GET', 'POST'])
def generator(location, descriptor,email,customer,reservation,order,route,manager):

        #Integrate SQL connection and custom prompts for user happiness level.

        form = Form()

        if request.method == 'GET':
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                n=1,
                messages=[
                    {"role": "system", "content": "You are a bot designed to write restaurant reviews that are positive and concise. Ensure they are only a single paragraph."},
                    {"role": "user", "content": "These reviews may be about the following restaurants: City Slice or City Pork."},
                    {"role": "assistant", "content": "City Slice and City Pork are restaurants located in Baton Rouge, Louisiana. They are members of parent company City Group Hospitality."},
                    {"role": "user", "content": "Write me a restaurant review for {} based on the following criteria: {}. Be sure to include the specific meal ordered. The meal specific meal ordered is the following: {} ".format(location,descriptor,order)}
                ]
            )

            global response
            response = resp['choices'][0]['message']['content']

            return render_template('generator.html', response=response, form=form)

        else:
            if 'accept' in request.form:

               email_address = "citytester4125@gmail.com"
               msg = EmailMessage()
               msg.set_content("Thank you for dining at {}! Please consider leaving a review, we have generated one based on the feedback given to our manager by you.\n{}".format(location,response))
               msg['Subject'] = "City Group Hospitality would like to thank you!"
               msg['From'] = "citytester4125@gmail.com"
               msg['To'] = email


               with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                   smtp.login(email_address, email_password)
                   smtp.send_message(msg)

               #if route == 'manager':
                   #writer(location,descriptor,email,customer,reservation,order,response)

               #else:
                   #pass

               return render_template('confirmation.html',response=response,email=email,route=route)
            else:
               return redirect(url_for('home'))


@app.route('/manager', methods=['GET', 'POST'])
def manager():
    #seperate from customer
   form = CustomerForm(request.form)
   if request.method == 'POST':
       reservation = request.form.get('reservation')
       location = request.form.get('location')
       customer = request.form.get('customer')
       manager = request.form.get('manager')
       email = request.form.get('email')
       order = request.form.get('order')
       descriptor = request.form.get('descriptor')

       if form.validate():
           route = 'manager'
           return redirect(url_for('generator', reservation=reservation,location=location, descriptor=descriptor, email=email,customer=customer,order=order,route=route,manager=manager))
       #else:
           #return render_template('manager.html', form=form,options=options,optionmanager=optionmanager,optionlocation=optionlocation)
   #else:
       #return render_template('manager.html', form=form,options=options,optionmanager=optionmanager,optionlocation=optionlocation)


@app.route('/customer', methods=['POST', 'GET'])
def customer():
    #potential customer happiness slider bar? Differentiate from manager.
   form = CustomerForm(request.form)
   if request.method == 'POST':
       location = request.form.get('location')
       email = request.form.get('email')
       order = request.form.get('order')
       descriptor = request.form.get('descriptor')

       if form.validate():
           route = 'customer'
           return redirect(url_for('generator',reservation='notprovided',location=location, descriptor=descriptor, email=email,customer='notprovided',order=order,route=route,manager='notprovided'))
       else:
           return render_template('customer.html', form=form)
   else:
       return render_template('customer.html', form=form)
