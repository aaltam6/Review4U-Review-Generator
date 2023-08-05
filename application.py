#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:11:32 2023

@author: arturoaltamirano808
"""
from flask import Flask, render_template, request,send_file
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms import Form,StringField,SubmitField
from wtforms.validators import InputRequired
import os
import pandas as pd
from pandas import ExcelWriter
from io import BytesIO
import openpyxl
import secrets

app = Flask(__name__)

class UploadForm(FlaskForm):
    file = FileField('Choose a file')
    submit = SubmitField('Upload')
    column = StringField('column', validators=[InputRequired()])
    values = StringField('values', validators=[InputRequired()])
    output = StringField('output', validators=[InputRequired()])


app.secret_key = secrets.token_hex(32)

def generator(file, column, *args):
    excel_file = pd.read_excel(file)

    # Group by specified column
    grouped = excel_file.groupby(column)

    # Create ExcelWriter object and save data to excel_stream
    excel_stream = BytesIO()
    writer = ExcelWriter(excel_stream)
    #list comprehension sorts "grouped" for values specified and writes via writer
    for x, y in grouped:
        if any(arg == x for arg in args):
            y.to_excel(writer, x, index=False)
    writer.close()

    # Reset the BytesIO object's position to the beginning
    excel_stream.seek(0)

    #return bytestream
    return excel_stream


@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadForm()
    if request.method == 'POST':
        file = request.files['file']
        
        #retrieve column
        column = request.form.get('column')

        #retrieve desired name of generated file
        output_name = request.form.get('output')

        #specified values to filter from column
        values = request.form.get('values')

        #split specified value list by "," character
        list_values = values.split(",")

        #assign excel_stream to generator call, pass target file, desired column, and desired filter values
        excel_stream = generator(file,column,*list_values)
        
        #return response variable with send_file command assigned as an attachment
        response = send_file (
                excel_stream,
                as_attachment=True,
                download_name = output_name + '.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        return response
        
    else:
        return render_template('home.html',form=form)

@app.route("/about", methods=['GET', 'POST'])
def about():
    if request.method == 'GET':
        return render_template('about.html')
