from pypdf import PdfReader
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import google.generativeai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer
import time
import random
import os
from dotenv import load_dotenv
import getpass

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
os.environ["TESSDATA_PREFIX"] = "C:/Program Files/Tesseract-OCR/tessdata"

poppler_path = "poppler-24.08.0/Library/bin"

DIRECCION_ACTUAL = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(DIRECCION_ACTUAL, '..', '..'))
env_path = os.path.join(root_dir, '.env')
load_dotenv()

API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    API_KEY = getpass.getpass("Enter API key for Google Gemini: ")

genai.configure(api_key=API_KEY)

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    def embed_documents(self, texts):
        return self.model.encode(texts, convert_to_numpy=True).tolist()
    def embed_query(self, text):
        return self.model.encode([text], convert_to_numpy=True)[0].tolist()

def extraer_texto_hibrido(pdf_path):
    reader = PdfReader(pdf_path)
    texto_completo = ""

    for i, page in enumerate(reader.pages):
        texto_completo += f"\n--- Página {i+1} ---\n"
        texto = page.extract_text()
        if texto and texto.strip():
            texto_completo += texto + "\n"
        else:
            imagen = convert_from_path(
                pdf_path,
                dpi=200,
                first_page=i+1,
                last_page=i+1,
                poppler_path=poppler_path
            )[0]
            ocr_text = pytesseract.image_to_string(imagen, lang="spa")
            texto_completo += "[Texto extraído con OCR]\n" + ocr_text + "\n"

    return texto_completo

def construir_base_conocimiento(pdf_paths, modo="rebuild"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    embedding_model = SentenceTransformerEmbeddings()

    if modo == "rebuild":
        print("Reconstruyendo la base de conocimiento")
        textos = [extraer_texto_hibrido(path) for path in pdf_paths]
        texto_completo = "\n".join(textos)
        chunks = splitter.split_text(texto_completo)

        vectorstore = FAISS.from_texts(chunks, embedding_model)
        vectorstore.save_local(os.path.join(DIRECCION_ACTUAL,"temp_db"))

    elif modo == "add":
        print("Agregando nuevos documentos a la base")
        vectorstore, embedding_model = cargar_base_conocimiento()
        for path in pdf_paths:
            texto = extraer_texto_hibrido(path)
            chunks = splitter.split_text(texto)
            new_vectorstore = FAISS.from_texts(chunks, embedding_model)
            vectorstore.merge_from(new_vectorstore)
        vectorstore.save_local(os.path.join(DIRECCION_ACTUAL, "temp_db"))

    return cargar_base_conocimiento()

def cargar_base_conocimiento():
    embedding_model = SentenceTransformerEmbeddings()
    vectorstore = FAISS.load_local(os.path.join(DIRECCION_ACTUAL, "temp_db"), embeddings=embedding_model, allow_dangerous_deserialization=True)
    return vectorstore, embedding_model

def buscar_contexto(pregunta, vectorstore, embedding_model, top_k=5):
    query_vector = embedding_model.embed_query(pregunta)
    docs_similares = vectorstore.similarity_search_by_vector(query_vector, k=top_k)
    return "\n".join([doc.page_content for doc in docs_similares])

def obtener_modelo_disponible():
    return "gemini-2.5-flash"

def responder_con_gemini(solicitud, vectorstore, embedding_model, reintentos=3, formato=1):
    contexto = buscar_contexto(solicitud, vectorstore, embedding_model)
    if len(contexto) > 5000:
        contexto = contexto[:5000]

    print("\n Fragmento de contexto:\n", contexto[:1000], "\n")

    # (Tu prompt sigue siendo el mismo)
    prompt = f"""
    Eres un asistente experto encargado de responder lo que se solicita basándote únicamente en la información proporcionada en el contexto. 
    No uses conocimientos previos ni infieras nada que no esté en el contexto.
    
    Contexto: {contexto}
    Solicitud:  {solicitud}
    
    Instrucciones:
    - Responde únicamente con la información encontrada en el contexto.
    - Si la respuesta no está en el contexto, responde exactamente: "La información no está disponible en los documentos proporcionados."
    - No agregues explicaciones adicionales, opiniones o comentarios.
    - Responde de manera clara y concisa.
    """

    if formato != 1:
        prompt = prompt + """
        
        Dado el contexto, responde en formato JSON la información que se te pide en la solicitud para llenar un registro de la siguiente tabla para la base de datos:

        CREATE TABLE Postulantes (
            id_postulante INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido_paterno VARCHAR(50) NOT NULL,
            apellido_materno VARCHAR(50),
            fecha_nacimiento DATE NOT NULL,
            curp CHAR(18) UNIQUE NOT NULL,
            rfc CHAR(13),
            correo VARCHAR(100),
            telefono VARCHAR(15),
            domicilio VARCHAR(200),
            fecha_postulacion DATE DEFAULT (CURRENT_DATE)
        );

        las claves del JSON deben ser las mismas que los atributos de las tablas, con excepción de id_postulante y fecha_postulacion
        Si algun dato permite null y no es encontrado para ser ingresado, entonces el contenido de dicho atributo será null.
        Considerando que la fecha de nacimiento debe estar en el formato DATE de MySQL.
        Considera que no debes agregar el texto de la siguiente forma:
        ```json
        {
            "key":"value"
        }
        ```
        Debe ser:
        {
            "key":"value"
        }
        """

    modelo_id = obtener_modelo_disponible()
    modelo = genai.GenerativeModel(modelo_id)

    for intento in range(reintentos):
        try:
            respuesta = modelo.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7, top_p=0.95, top_k=40, max_output_tokens=1024
                )
            )
            # 1. Verificar si hay candidatos en la respuesta
            if not respuesta.candidates:
                # Esto puede pasar si el PROMPT fue bloqueado
                print("Error: El prompt fue bloqueado, no hubo candidatos.")
                # Intenta obtener la razón del bloqueo del prompt si existe
                try:
                    razon_prompt = respuesta.prompt_feedback.block_reason.name
                    return f"Error: El prompt fue bloqueado por: {razon_prompt}"
                except Exception:
                    return "Error: El prompt fue bloqueado (razón desconocida)."

            candidate = respuesta.candidates[0]

            # 2. Verificar la razón de finalización (1=STOP, 2=MAX_TOKENS, 3=SAFETY, 4=RECITATION)
            #    Tratamos 1 (STOP) y 2 (MAX_TOKENS) como respuestas válidas.
            if candidate.finish_reason != 1 and candidate.finish_reason != 2:
                print(f"Error: La respuesta fue bloqueada. Razón: {candidate.finish_reason.name}")
                return f"Error: La respuesta fue bloqueada por: {candidate.finish_reason.name}"

            # 3. Verificar si hay contenido (parts)
            if not candidate.content or not candidate.content.parts:
                print("Error: El modelo devolvió una respuesta vacía (probablemente por SAFETY).")
                return "Error: La respuesta del modelo estaba vacía (bloqueada por seguridad)."
            
            # 4. Si todo está bien, AHORA SÍ, acceder al texto
            return candidate.content.parts[0].text

        except Exception as e:
            if "429" in str(e):
                espera = 60 + random.randint(0, 10)
                print(f"Esperando {espera} segundos por límite de cuota...")
                time.sleep(espera)
            else:
                # Imprime el error real (el que te salió)
                print(f"Error no manejado en generate_content: {e}") 
                break

    return "Ocurrió un error generando la respuesta. Intenta más tarde."

def respuesta_simple_con_gemini(solicitud, reintentos=3):

    prompt = f"""
    Eres un asistente inmobiliario amable y profesional. Ayuda a los usuarios a encontrar propiedades como casas,
    departamentos, villas o condominios según su ubicación, presupuesto y número de recámaras.
    Solo puedes responder preguntas relacionadas con la compra, venta o renta de propiedades como casas, departamentos, villas o condominios.
    Si te preguntan sobre temas ajenos (como historia, tecnología o ciencia), responde educadamente que solo puedes ayudar con bienes raíces.

    Solicitud: {solicitud}
    """

    modelo_id = obtener_modelo_disponible()
    modelo = genai.GenerativeModel(modelo_id)

    for intento in range(reintentos):
        try:
            respuesta = modelo.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7, top_p=0.95, top_k=40, max_output_tokens=1024
                )
            )
            return respuesta.text
        except Exception as e:
            if "429" in str(e):
                espera = 60 + random.randint(0, 10)
                print(f"Esperando {espera} segundos por límite de cuota...")
                time.sleep(espera)
            else:
                print("Error no manejado:", e)
                break

    return "Ocurrió un error generando la respuesta. Intenta más tarde."

if __name__ == "__main__":
    pdf_dir = os.path.join(DIRECCION_ACTUAL, "PDF")

    # Listar los PDFs que estén en la carpeta
    pdfs = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

    modo = "add"

    vectorstore, embedding_model = construir_base_conocimiento(pdfs)

    pregunta = "En los documentos proporcionados, ¿cuál es la fecha de nacimiento de la persona?"
    respuesta = responder_con_gemini(pregunta, vectorstore, embedding_model)

    print("\nPregunta:", pregunta)
    print("Respuesta:", respuesta)