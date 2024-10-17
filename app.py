import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL='postgresql://luis:dxzIQn3Kzuz2iGUa8fll12IhsE1m3h5y@dpg-cs8j3n08fa8c73buov9g-a.oregon-postgres.render.com:5432/luis_hn9r'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo de la tabla 'estudiantes'
class Estudiante(db.Model):
    __tablename__ = 'alumnos'
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=True)
    ap_paterno = db.Column(db.String, nullable=True)
    ap_materno = db.Column(db.String, nullable=True)
    semestre = db.Column(db.Integer, nullable=True)

# Endpoint para obtener todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    estudiantes = Estudiante.query.all()
    lista_estudiantes = []
    for estudiante in estudiantes:
        lista_estudiantes.append({
            'no_control': estudiante.no_control,
            'nombre': estudiante.nombre,
            'ap_paterno': estudiante.ap_paterno,
            'ap_materno': estudiante.ap_materno,
            'semestre': estudiante.semestre
        })
    return jsonify(lista_estudiantes)

# Endpoint para agregar un nuevo estudiante
@app.route('/estudiantes', methods=['POST'])
def agregar_estudiante():
    data = request.get_json()
    nuevo_estudiante = Estudiante(
        no_control=data['no_control'],
        nombre=data['nombre'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        semestre=data['semestre']
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return jsonify({'mensaje': 'Estudiante agregado exitosamente'}), 201

# Endpoint para obtener un estudiante por no_control
@app.route('/estudiantes/<no_control>', methods=['GET'])
def obtener_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante is None:
        return jsonify({'mensaje': 'Estudiante no encontrado'}), 404
    return jsonify({
        'no_control': estudiante.no_control,
        'nombre': estudiante.nombre,
        'ap_paterno': estudiante.ap_paterno,
        'ap_materno': estudiante.ap_materno,
        'semestre': estudiante.semestre
    })

# Endpoint para actualizar un estudiante
@app.route('/estudiantes/<no_control>', methods=['PUT'])
def actualizar_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante is None:
        return jsonify({'mensaje': 'Estudiante no encontrado'}), 404
    data = request.get_json()
    estudiante.nombre = data['nombre']
    estudiante.ap_paterno = data['ap_paterno']
    estudiante.ap_materno = data['ap_materno']
    estudiante.semestre = data['semestre']
    db.session.commit()
    return jsonify({'mensaje': 'Estudiante actualizado exitosamente'})

# Endpoint para eliminar un estudiante
@app.route('/estudiantes/<no_control>', methods=['DELETE'])
def eliminar_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if estudiante is None:
        return jsonify({'mensaje': 'Estudiante no encontrado'}), 404
    db.session.delete(estudiante)
    db.session.commit()
    return jsonify({'mensaje': 'Estudiante eliminado exitosamente'})

if __name__ == '__main__':
    app.run(debug=True)