from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)

mysql = MySQL()


app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.config['MYSQL_DATABASE_USER'] = 'root'

app.config['MYSQL_DATABASE_PASSWORD'] = ''

app.config['MYSQL_DATABASE_BD'] = 'sistema'

mysql.init_app(app)

#Routing
@app.route('/')
def index():
   
    return render_template('empleados/index.html')



@app.route('/create')
def create():
    return render_template('empleados/create.html')


@app.route('/store', methods=["POST"])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    
    now = datetime.now()

    tiempo = now.strftime("%Y%H%M%S")
    
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
        
    datos = (_nombre, _correo, nuevoNombreFoto)
    
    print(datos)
    
    #OJO van backticks en los campos en lugar de '' 
    sql = "INSERT INTO `sistema`.`empleados`\
        (`id`, `nombre`, `correo`, `foto`)\
        VALUES (NULL, %s, %s, %s);"
    
    conn = mysql.connect()
    
    cursor = conn.cursor()
    
    cursor.execute(sql, datos)
    
    conn.commit()
    
    return render_template('empleados/create.html')    
    
@app.route('/listaEmpleados')
def cargarEmpleados():
    sql="SELECT * FROM `sistema`.`empleados`;" 
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    db_empleados = cursor.fetchall()
    conn.commit() 
    return render_template('empleados/listaEmpleados.html', empleados = db_empleados)   

@app.route('/destroy/<int:id>')
def destroy(id):
    sql = "DELETE FROM `sistema`.`empleados` WHERE `id` = %s"
    datos = str(id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit() 
    
    return redirect("/listaEmpleados")

if  __name__ == '__main__':
    app.run(debug=True) 
    

