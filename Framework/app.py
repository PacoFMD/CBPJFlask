import psycopg2
from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:geda89031129gp@localhost/comision'
#db = SQLAlchemy(app)
global connection
values = ["Hombre","Otro","Otre"] 
app.debug = True
# para crear una tabla 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile/<username>')
def profile(username):
    connection = psycopg2.connect(user="postgres",password="geda89031129gp",host="localhost",port="5432",database="comision")
       
    try:
        cursor = connection.cursor()
        sql_select_query = """SELECT *FROM usuarios WHERE "IdUsuarios" = %s"""
        cursor.execute(sql_select_query,(username))
        record = cursor.fetchone()           
        print(record)
        return render_template('profile.html',usuario=record) 
    except (Exception,psycopg2.Error) as error: 
        if(connection):
            print("Failed", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("Close connection")
              
    return "error"


@app.route('/acceder', methods=['POST'])
def acceder():
    connection = psycopg2.connect(user="postgres",password="geda89031129gp",host="localhost",port="5432",database="comision")     
    print(request.form['password'])
    print(request.form['usuario'])    
    try:
        cursor = connection.cursor()
        sql_select_query = """SELECT *FROM usuarios WHERE "Nombre_Usuario" = %s AND "Password" = %s"""
        cursor.execute(sql_select_query,(request.form['usuario'],request.form['password']))
        record = cursor.fetchone()
        print(record)
        
        if record != None:   
            return render_template('Registro.html',usuario=record)
        else:
            return render_template('index.html')   
    except (Exception,psycopg2.Error) as error: 
        if(connection):
            print("Failed", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("Close connection")
    return "error"    

@app.route('/buscar')
def buscar():
    return render_template('Busqueda.html') 


@app.route('/post_user', methods=['POST'])
def post_user():
    connection = psycopg2.connect(user="postgres",password="geda89031129gp",host="localhost",port="5432",database="comision")    
    try:
        cursor = connection.cursor()
        postgres_insert_query = """INSERT INTO usuarios ("Nombre_Usuario","Password") VALUES (%s,%s)"""
        #  user = 
        #  password = request.form['password']
        record_to_insert=(request.form['username'],request.form['password'])
        cursor.execute(postgres_insert_query,record_to_insert)
        connection.commit()
        print("Success")
    except (Exception,psycopg2.Error) as error: 
        if(connection):
            print("Failed", error)
    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("Close connection")
    return redirect(url_for('index'))       
     

@app.route('/registro')
def registro():
    return render_template('Registro.html')
if __name__ == "__main__":
    app.run()