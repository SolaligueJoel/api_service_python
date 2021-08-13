import traceback
import traceback
import os


from flask import Flask, request, jsonify, render_template, Response, redirect
from sqlalchemy.sql.operators import is_distinct_from
import os
from flask import Flask, request, jsonify, render_template, Response, redirect
from config import config
from usuario import db
import traceback
import usuario


# Init app
app = Flask(__name__)
script_path = os.path.dirname(os.path.realpath(__file__))
# Get the parameters 
config_path_name = os.path.join(script_path, 'config.ini')
db_config = config('db', config_path_name)
server_config = config('server', config_path_name)
# Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_config['database']}"
# Initi db
db.init_app(app)


@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        result  = "<h2>Endpoints disponibles:</h2>"
        result += "<h3>[GET] /user/{id}/titles --> titulos completados por usuario con id pasado por parametro</h3>"
        result += "<h3>[GET] /user/graph --> reporte mediante grafico de cuantos titulos completó cada usuario</h3>"
        result += "<h3>[GET] /user/titles --> informar mediante un json cuantos titulos completó cada usuario"
        
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/reset")
def reset():
        try:
            # Borrar y crear la base de datos
            usuario.clear()
            usuario.fill()
            result = "<h3>Base de datos re-generada!</h3>"
            return (result)
        except:
            return jsonify({'trace': traceback.format_exc()})

@app.route("/user/<id>/titles")
def user(id):
        try:
            return (f"<h3>El usuario {id} completo: {usuario.title_completed_count(id)} titulos.</h3>")            
        except:
            return jsonify([{'trace': traceback.format_exc()}])

@app.route("/user/graph")
def graph():
    return usuario.graph_title()


@app.route("/user/titles")
def title():
    return jsonify(usuario.json_title())



if __name__ == "__main__":
    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)