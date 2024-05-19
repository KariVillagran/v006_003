from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from config import config


app =  Flask(__name__)
conexion = MySQL(app)



@app.route('/herramientas', methods=[''])
def listar_herramientas():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, precio, descripcion FROM herramientas"
        cursor.execute(sql)
        datos=cursor.fetchall()   
        herramientas=[]
        for fila in datos:
            herramienta={'codigo':fila[0], 'nombre':fila[1], 'precio':fila[2], 'descripcion':fila[3]}
            herramientas.append(herramienta)
        return jsonify({'herramientas':herramientas, 'mensaje':"herramientas listadas!"})

    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@app.route('/herramientas/<codigo>', methods=['GET'])
def leer_herramientas(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, precio, descripcion FROM herramientas WHERE codigo = '{0}' ".format(codigo)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            herramienta={'codigo': datos[0], 'nombre':datos[1], 'precio':datos[2], 'descripcion':datos[3]}            
            return jsonify({'herramienta':herramienta, 'mensaje':"herramientas listadas!"})
        else:
            return jsonify({'mensaje': "Herramienta no encontrada wn"})

    except Exception as ex:
        return jsonify({'mensaje':"Error"}) 





@app.route('/herramientas',methods=['POST'])
def registrar_herramienta():
    try:
        #print(request.json)
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO herramientas (codigo, nombre, precio, descripcion)
        VALUES ({0},'{1}',{2},'{3}')""".format(request.json['codigo'],request.json['nombre'],
                                               request.json['precio'],request.json['descripcion'])
        cursor.execute(sql)
        conexion.connection.commit() #Confirmacion de query                
        return jsonify({'mensaje': "herramienta registrada"})
    
    except Exception as ex:
        return jsonify({'mensaje' : "Error" })

@app.route('/herramientas/<codigo>', methods=['DELETE'])
def eliminar_herramienta(codigo):
        try:
        #print(request.json)
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM herramientas WHERE codigo = '{0}' ".format(codigo)
            cursor.execute(sql)
            conexion.connection.commit() #Confirmacion de query                
            return jsonify({'mensaje': "herramienta eliminada"})
    
        except Exception as ex:
            return jsonify({'mensaje' : "Error" })


@app.route('/herramientas/<codigo>', methods=['PUT'])
def actualizar_herramienta(codigo):
    try:
        #print(request.json)
        cursor = conexion.connection.cursor()
        sql = """ UPDATE herramientas SET nombre = '{0}', precio = {1} 
        WHERE codigo = '{2}'""".format(request.json['nombre'],request.json['precio'], codigo)
        cursor.execute(sql)
        conexion.connection.commit() #Confirmacion de query                
        return jsonify({'mensaje': "herramienta actualizada"})
    
    except Exception as ex:
        return jsonify({'mensaje' : "Error" })
    





def no_encontrada(error):
    return "<h4>La pagina buscada no existe..</h4>",404




if __name__ == '__main__':
    app.config.from_object(config['develoment'])
    app.register_error_handler(404, no_encontrada)
    app.run()