from flask import Flask, render_template, request, redirect,url_for, flash
from flask_mysqldb import MySQL
#from flask_socketio import SocketIO, send

app = Flask(__name__)

#Siempre tener activado Laragon, y la BDD esta en MySQL
app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskcontacts'
mysql = MySQL(app)


#Configuraciones de Sesion
app.secret_key = 'mysecretkey'

#socketiocon = SocketIO(app)



#Rutas
##Esta ruta solo es / porque es la pinrcipal
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/formregistro')
def formregistro():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('userregister.html', contacts = data)

@app.route('/addcontact', methods=['POST'])
def addcontact():
    if request.method == 'POST':#se revisa si se entro a la ruta con datos por medio del metodo POST
        #se reciben los datos ingresados en el formulario
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phonenumber = request.form['phone']
        email = request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (firstname, lastname, phone, email) VALUES (%s, %s, %s, %s)', 
        (firstname, lastname, phonenumber, email))
        mysql.connection.commit()
        #flash permite enviar mensajes entre rutas
        flash('Contacto Agregado Satisfactoriamente')
        return redirect(url_for('formregistro'))

@app.route('/edit/<id>')
def getcontact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id={0}'.format(id))
    #cuando solo se consulta un usuario o tuple, se obtiene una lista dentro de otra lista
    #por eso se enviara el indice 0, el cual es la lista con los datos del susuario a editar
    #descomentar el print para comprender
    data = cur.fetchall()
    #print(data[0])
    return render_template('editcontact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def updatecontact(id):
    if request.method == 'POST':#se revisa si se entro a la ruta con datos por medio del metodo POST
        #se reciben los datos ingresados en el formulario de editar contacto
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phonenumber = request.form['phone']
        email = request.form['email']
        cur =  mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET firstname = %s,
                lastname = %s,
                phone = %s,
                email = %s
            WHERE id = %s
        """, (firstname, lastname, phonenumber, email,id))
        mysql.connection.commit()
        flash('El contacto fue editado con exito')
        return redirect(url_for('formregistro'))

@app.route('/delete/<string:id>')
def deletecontact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash('Contacto removido satisfactoriamente')
    return redirect(url_for('formregistro'))


##@socketiocon.on('message')
##def handleMessage(msg):
##    print("El mensaje enviado es: "+msg)
##    send(msg, broadcast=True)


##Evalua que el archivo que se esta ejecutando sea el main y no un modulo
if __name__=='__main__':
    app.run()##si es asi, se ejecuta la aplicacion
    #si se quiere usar el socket se tiene que dejar de usar el app run
    #socketiocon.run(app)