from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from LLM.base_llm import cargar_base_conocimiento, construir_base_conocimiento, responder_con_gemini, respuesta_simple_con_gemini
from LLM.SQL_Agent import getResponse
from config.db import DB, CantidadVista, TipoConsulta
import os
from langchain_community.utilities import SQLDatabase
import json
from sqlalchemy import text

BASE_DIR = os.path.dirname(__file__)
APP_FOLDER = os.path.join(BASE_DIR, "app")

app = Flask(__name__,
            template_folder=os.path.join(APP_FOLDER, "templates"),
            static_folder=os.path.join(APP_FOLDER, "static"))
CORS(app) 

flag = True

# Carpeta donde se almacenan los PDFs
PDF_FOLDER = os.path.join(BASE_DIR, "PDF")
os.makedirs(PDF_FOLDER, exist_ok=True)

# Chat inmobiliario
@app.route("/chat_inmobiliario", methods=["POST"])
def chat_inmobiliario():
    global flag

    data = request.get_json()
    pregunta = data.get("mensaje", "")
    respuesta = respuesta_simple_con_gemini(pregunta)
 
    return jsonify({"respuesta": respuesta})  

# Chat
@app.route("/chat", methods=["POST"])
def chat():
    global flag

    data = request.get_json()
    pregunta = data.get("mensaje", "")

    if flag:
        respuesta = getResponse(pregunta) 
    else:
        vectorstore, embedding_model = cargar_base_conocimiento()
        respuesta = responder_con_gemini(pregunta, vectorstore, embedding_model)
        flag = True
 
    return jsonify({"respuesta": respuesta})  

# Archivos PDF
@app.route("/upload_to_chat", methods=["POST"])
def upload_file_in_chat():
    global flag
    # Validaciones
    if "file" not in request.files:
        return jsonify({"respuesta": "No se envió ningún archivo"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"respuesta": "Archivo sin nombre"}), 400

    # Guardar PDF en carpeta local
    file_path = os.path.join(PDF_FOLDER, file.filename)
    file.save(file_path)

    # Actualizar base de conocimiento con el nuevo PDF
    vectorstore, embedding_model = construir_base_conocimiento([file_path], modo="rebuild")
    flag = False

    return jsonify({"respuesta": f"Archivo '{file.filename}' agregado a la base de conocimiento"})

# Archivos PDF
@app.route("/upload", methods=["POST"])
def upload_file():

    # Validaciones
    if "file" not in request.files:
        return jsonify({"respuesta": "No se envió ningún archivo"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"respuesta": "Archivo sin nombre"}), 400

    # Guardar PDF en carpeta local
    file_path = os.path.join(PDF_FOLDER, file.filename)
    file.save(file_path)

    # Actualizar base de conocimiento con el nuevo PDF
    vectorstore, embedding_model = construir_base_conocimiento([file_path], modo="rebuild")

    solicitud = """
    Dime el nombre/s, apellido paterno, apellido materno, fecha de nacimiento, curp, rfc, correo electrónico,
    telefono y domicilio de la persona a la cual pertenecen los documentos que se encuentran.
    """
    dict = responder_con_gemini(solicitud, vectorstore, embedding_model, formato = 2)

    print("\nRespuesta de Gemini:\n")
    print(dict)

    dict = json.loads(dict) # La respuesta de gemini se convierte a un diccionario

    columnas = dict.keys() # Se obtienen las claves

    cols_str = ", ".join(columnas)  # Se unen las claves separadas por coma en un string

    placeholders_str = ", ".join(f":{col}" for col in columnas) # Se unen los atributos

    sql_query = text(f"""
        INSERT INTO Postulantes ({cols_str}) 
        VALUES ({placeholders_str})
    """) # Se elabora la query

    print("\nConsulta a ejecutar:")
    print(sql_query)

    db_uri = "mysql+mysqlconnector://root:1234@127.0.0.1:3307/bd_corporativa_simulada"

    db = SQLDatabase.from_uri(db_uri) # Se realiza la conexión a la base de datos

    print("\nInsertando datos...")
    with db._engine.connect() as conexion:
        # SQLAlchemy se encarga de mapear :nombre con postulante_datos["nombre"]
        conexion.execute(sql_query, dict)
        conexion.commit()

    print("¡Postulante insertado correctamente!")

    return jsonify({"respuesta": f"Archivo '{file.filename}' agregado a la base de conocimiento"})

# Interfaz
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<path:filename>")
def serve_html(filename):
    if filename.endswith('.html'):
            return render_template(filename)

# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    consulta = """
    SELECT 1 FROM Usuarios where correo = ? and contrasena = ? 
    """
    resultado = DB.consultas(consulta, TipoConsulta.SELECT, CantidadVista.ONE, 10, correo, contrasena)

    if resultado == []:
        return jsonify({"estatus": 0})
    return jsonify({"estatus": 1})

if __name__ == "__main__":
    app.run(debug=True)  
