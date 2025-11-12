# Python libraries
import os
import sqlite3
from enum import Enum
from typing import Optional, List, Any

DB_FILE = "login.db"

class CantidadVista(Enum):
    ALL = 1
    ONE = 2
    MANY = 3

class TipoConsulta(Enum):
    SELECT = 1
    OTHER = 2

class DB:
    connection = None
    is_first_time = True
    
    def __init__(self):
        self.db_name = os.path.normpath(os.path.join(os.path.abspath(__file__), "../..", "login.db"))
    
    def __enter__(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None: 
            self.connection.close()
            self.connection = None

    def close_connection(self) -> None:
        self.connection = None

    @staticmethod
    def format_result(data: Optional[List[sqlite3.Row]]) -> Optional[List[dict[str, Any]]]:
        print([resultados for resultados in data])
        return None if data is None else [dict(resultados) for resultados in data]

    @staticmethod
    def consultas(peticion: str, tipo: TipoConsulta, options: CantidadVista = CantidadVista.ALL, cantidad=10, *condiciones) -> Optional[List[dict[str, Any]]]:
        resultado = None
        try:
            with DB() as con:
                cursor = con.cursor()
                query = cursor.execute(peticion, condiciones)

                if tipo == TipoConsulta.SELECT:
                    if CantidadVista.ONE == options:
                        fila = query.fetchone()
                        if fila:
                            resultado = [dict(fila)]
                        else:
                            resultado = []
                    elif CantidadVista.MANY == options:
                        resultado = DB.format_result(query.fetchmany(cantidad))
                    else:
                        resultado = DB.format_result(query.fetchall())
                else:
                    con.commit()
        except sqlite3.Error as SQLe:
           print(f"Ha ocurrido un error en la consulta: {SQLe}")
        return resultado

    def crear_bd(self):
        if self.is_first_time:
            print("Se está creando la base de datos")
            self.is_first_time = False
            try:
                with DB() as con:
                    cursor = con.cursor()
                    cursor.execute("CREATE TABLE Usuarios(id INTEGER PRIMARY KEY, correo VARCHAR(250), contrasena VARCHAR(250))")
                    cursor.execute("insert into Usuarios(correo, contrasena) values ('luisreyes@gmail.com', '123456')")

                    con.commit()

            except sqlite3.Error as sqlE: 
                print(f"Error en SQLite: {sqlE}")
            except Exception as e:
                print(f"Ha ocurrido un error: {e}")
        return

if __name__ == "__main__":
    print("Probando segmento de código")
    base_datos = DB()
    base_datos.crear_bd()

    element = DB().consultas("SELECT * FROM Usuarios", TipoConsulta.SELECT, CantidadVista.MANY)
    element_dict = [dict(row) for row in element] if element is not None else []
    print(element_dict)