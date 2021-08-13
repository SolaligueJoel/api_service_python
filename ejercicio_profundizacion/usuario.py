from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from flask import Response


db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "listado"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String)
    title = db.Column(db.String)
    completed = db.Column(db.String)
    
    def __repr__(self):
        return f"User:{self.userId}, Title:{self.title}, Completed:{self.completed}"

def clear():
    db.drop_all()
    db.create_all()

def fill():
    url = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(url)
    data_json = response.json()
    for x in data_json:
        producto = Usuario(userId=x["userId"],title=x["title"],completed=x["completed"])    
        db.session.add(producto)
        db.session.commit()
    
    
def title_completed_count(id):
    user_true = db.session.query(Usuario).filter((Usuario.userId == id) & (Usuario.completed==1)).count()
    return user_true


def graph_title():
    users = db.session.query(Usuario).all()
    
    new_list = [int(x.userId) for x in users if x.completed == "1"]
    new_dict = dict(zip(new_list,map(lambda x: new_list.count(x),new_list)))
    len_list = len(new_dict.keys())+1

    fig = Figure(figsize= (15,8))
    fig.tight_layout()
    
    ax = fig.add_subplot()
    ax.set_title("Comparando titulos completados por UserId")
    ax.bar(new_dict.keys(),new_dict.values())
    ax.set_facecolor("bisque")
    ax.set_xticks(range(1,len_list,1))
    
    ax.set_title('Titulos completados por Id')
    ax.set_xlabel('User Ids')
    ax.set_ylabel('Cantidad Titulos')
    
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
        
    return Response(output.getvalue(), mimetype='image/png') 
        
    
def json_title():
    users = db.session.query(Usuario).all()
    
    new_list = [int(x.userId) for x in users if x.completed == "1"]
    new_dict = dict(zip(new_list,map(lambda x: new_list.count(x),new_list)))
    new_data = []
    for x in new_dict:
        new_data.append((f"El usuario {x} completo: {(new_dict[x])} titulos"))
        
    with open ('data.json','w') as file:
        json.dump(new_data,file,indent=4)
    return new_data
