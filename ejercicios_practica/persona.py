#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 1.2

Descripcion:
Programa creado para administrar la base de datos de registro de personas
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.2"


from flask import json
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Response
from matplotlib.figure import Figure
import numpy as np
from collections import OrderedDict


from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import send_file
db = SQLAlchemy()

class Persona(db.Model):
    __tablename__ = "persona"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String)
    age = db.Column(Integer)
    nationality = db.Column(String)
    
    def __repr__(self):
        return f"Persona:{self.name} con nacionalidad {self.nationality}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(name, age, nationality):
    # Crear una nueva persona
    person = Persona(name=name, age=age, nationality=nationality)

    # Agregar la persona a la DB
    db.session.add(person)
    db.session.commit()


def report(limit=0, offset=0):
    # Obtener todas las personas
    query = db.session.query(Persona)
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    json_result_list = []

    # De los resultados obtenidos pasar a un diccionario
    # que luego será enviado como JSON
    # TIP --> la clase Persona podría tener una función
    # para pasar a JSON/diccionario
    for person in query:
        json_result = {'name': person.name, 'age': person.age, 'nationality': person.nationality}
        json_result_list.append(json_result)

    return json_result_list

def nationality_review():
    query = db.session.query(Persona)
    
    listnat = [x.nationality for x in query]
    listx = [x.id for x in query]
    listy = [x.age for x in query]
    new_listnat = list(OrderedDict.fromkeys(listnat))
    lenlist = int(len(listx)+1)
    
    count_list = []
    for x in new_listnat:
        count_list.append(listnat.count(x))
    
    
    
    fig = Figure(figsize=(15,7))
    fig.tight_layout()
    
    ax = fig.add_subplot(1,3,1)
    ax.set_title("Nacionalidades",fontsize=24)
    ax.pie(count_list,labels = new_listnat,autopct='%1.0f%%',shadow=True)
    ax.axis('equal')
    
    
    ax1 = fig.add_subplot(1,3,3)

    ax1.bar(listx,listy,color="purple")
    ax1.set_facecolor("bisque")
    ax1.set_xticks(range(1,lenlist,1))
    
    ax1.set_title('Edades',fontsize=24)
    ax1.set_xlabel('Ids')
    ax1.set_ylabel('Edad')
    
    
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
        
    return Response(output.getvalue(), mimetype='image/png') 
