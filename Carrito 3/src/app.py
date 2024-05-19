from flask import Blueprint, jsonify, request
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config



app =  Flask(__name__)
conexion = MySQL(app)


@app.route('/')
def index():
    return "carro API!"

@app.route('/cart', methods=['GET'])
def view_cart():
    try:
        cursor = conexion.connection.cursor()
        sql = """
            SELECT cart_items.id, herramientas.nombre, cart_items.quantity, herramientas.precio
            FROM cart_items
            JOIN herramientas ON cart_items.codigo = herramientas.codigo
        """
        cursor.execute(sql)
        cart_items = cursor.fetchall()
        cart = [{'id': item[0], 'nombre': item[1], 'cantidad': item[2], 'precio': item[3], 'total': item[2] * item[3]} for item in cart_items]
        return jsonify({'carro': cart, 'mensaje': "Elementos del carro listados"})
    except Exception as ex:
        return jsonify({'message': "Error"})

@app.route('/cart', methods=['POST'])
def add_to_cart():
    try:
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO cart_items (codigo, quantity) VALUES (%s, %s)"
        data = (request.json['codigo'], request.json['quantity'])
        cursor.execute(sql, data)
        conexion.connection.commit()
        return jsonify({'message': "Product added to cart"})
    except Exception as ex:
        return jsonify({'message': "Error"})

@app.route('/cart/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE cart_items SET quantity = %s WHERE id = %s"
        data = (request.json['quantity'], item_id)
        cursor.execute(sql, data)
        conexion.connection.commit()
        return jsonify({'mensaje': "items actualizados"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/cart/<int:item_id>', methods=['DELETE'])
def delete_cart_item(item_id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM cart_items WHERE id = %s"
        cursor.execute(sql, (item_id,))
        conexion.connection.commit()
        return jsonify({'message': "se ah eliminado el elemento"})
    except Exception as ex:
        return jsonify({'message': "Error"})


@app.errorhandler(404)
def page_not_found(error):
    return "<h4>La página buscada no existe.</h4>", 404


if __name__ == '__main__':
    app.config.from_object(config['develoment'])
    app.run()

