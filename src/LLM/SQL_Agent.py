from langchain_community.utilities import SQLDatabase
import getpass
import os
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_classic.schema import HumanMessage
from langchain_classic.agents import initialize_agent
from langchain_classic.agents.agent_types import AgentType
from langchain_classic.chat_models import init_chat_model 
from dotenv import load_dotenv

script_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
env_path = os.path.join(root_dir, '.env')
load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

db_uri = "mysql+mysqlconnector://root:1234@127.0.0.1:3307/bd_corporativa_simulada"

db = SQLDatabase.from_uri(db_uri)

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

system_message = """
Tú eres un agente diseñado para interactuar con una base de datos SQL.
Dada una pregunta realizada, crea una query sintacticamente correcta para {dialect} y ejecutala,
entonces mira los resultado de la query y desarrolla una respuesta. A menos que el usuario
especifique un numero de ejemplos que desee obtener, siempre limita los resultados de la query a
a lo mucho {top_k} resultados.

Puedes ordenar los resultado según una columna relevante para retornar los ejemplos mas
interesantes de la base de datos. Nunca consultes todas las columnas de una tabla específica,
solamente consulta las columnas relevantes dada la pregunta.

Tú DEBES checar más de una vez para asegurarte de que la query esté correcta antes de ejecutarla.
Si obtienes un error al ejecutar la query, entonces reescribe la query e intentalo de nuevo.

NO HAGAS ninguna sentencia DML (INSERT, UPDATE, DELETE, DROP, etc.) a la base de datos.

Para empezar SIEMPRE debes mirar las tablas en la base de datos para ver que puedes
consultar. NO TE SALTES ESTE PASO.
Después debes consultar el esquema de las tablas mas relevantes.
""".format(
    dialect="mysql",
    top_k=20,
)

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={
        'prefix': system_message
    }
)

def getResponse(question):
    return agent_executor.run(question)