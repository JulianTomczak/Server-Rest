from fastapi import FastAPI
from model.moderador_connection import ModeradorConnection
from model.denuncia_connection import DenunciaConnection
from schema.moderador_schema import ModeradorSchema
from schema.denuncia_schema import DenunciaSchema

app = FastAPI()
conn = ModeradorConnection()
conn2 = DenunciaConnection()

"""Denuncias"""

@app.get("/")
def root():
    items =[]
    for data in conn2.read_all():
        dictionary ={}
        dictionary["id"]= data[0]
        dictionary["motivo"]= data[1]
        dictionary["id_recipe"]= data[2]
        dictionary["resuelta"]= data[3]
        items.append(dictionary)
    return items

"""Moderadores"""

@app.get("/api/moderador")
def index():
    items = []
    for data in conn.read_all():
        dictionary ={}
        dictionary["id"]= data[0]
        dictionary["name"]= data[1]
        dictionary["last_name"]= data[2]
        dictionary["email"]= data[3]
        dictionary["username"]= data[4]
        dictionary["password"]= data[5]
        items.append(dictionary)
    return items

@app.get("/api/moderador/{id}")
def get_one(id:str):
    dictionary ={}
    data= conn.read_one(id)
    dictionary["id"]= data[0]
    dictionary["name"]= data[1]
    dictionary["last_name"]= data[2]
    dictionary["email"]= data[3]
    dictionary["username"]= data[4]
    dictionary["password"]= data[5]
    return dictionary

@app.post("/api/moderador/insert")
def insert(moderador_data: ModeradorSchema):
    data = moderador_data.model_dump()
    conn.write(data)

@app.put("/api/moderador/update/{id}")
def update(id:str, moderador_data: ModeradorSchema):
    data = moderador_data.model_dump()
    data["id"]=id
    conn.update(data)

@app.delete("/api/moderador/delete/{id}")
def delete(id:str):
    conn.delete(id)

"""Denuncias"""

@app.get("/api/denuncias/{id}")
def get_one(id:str):
    dictionary ={}
    data= conn2.read_one(id)
    dictionary["id"]= data[0]
    dictionary["motivo"]= data[1]
    dictionary["id_recipe"]= data[2]
    dictionary["resuelta"]= data[3]
    return dictionary

@app.post("/api/denuncias/insert")
def insert(denuncias_data: DenunciaSchema):
    data = denuncias_data.model_dump()
    conn2.write(data)

@app.put("/api/denuncias/update/{id}")
def update(id:str, denuncias_data: DenunciaSchema):
    data = denuncias_data.model_dump()
    data["id"]=id
    conn2.update(data)

@app.delete("/api/denuncias/delete/{id}")
def delete(id:str):
    conn2.delete(id)

"""Recipes"""

@app.delete("/api/recipes/delete/{id}")
def delete(id:str):
    conn2.delete(id)