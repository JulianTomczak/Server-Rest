from fastapi import FastAPI, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from model.moderador_connection import ModeradorConnection
from model.denuncia_connection import DenunciaConnection
from model.recipes_connection import RecipesConnection
from schema.moderador_schema import ModeradorSchema
from schema.denuncia_schema import DenunciaSchema
import psycopg2
from fastapi.templating import Jinja2Templates
from schema.mensaje_schema import SendMessage,ReplyMessage
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar el middleware CORS para permitir solicitudes desde el origen de tu aplicación React.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = psycopg2.connect(
    user="postgres",
    password="root",
    host="localhost",
    port='5432',
    database = "chefencasa"
)

cursor = db.cursor()

conn = ModeradorConnection()
conn2 = DenunciaConnection()
conn3 = RecipesConnection()
template = Jinja2Templates(directory="./view")

"""Inicio"""

@app.get("/")
def root(req: Request):
    return template.TemplateResponse("index.html", {"request": req})

@app.post("/", response_class=HTMLResponse)
def root(req: Request):
  return template.TemplateResponse("index.html", {"request": req})

@app.post("/api/denuncias", response_class=HTMLResponse)
def denuncias(req: Request,  username: str = Form(), password: str = Form()):
    user = conn.get_one(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    if user[5]!=password:
        raise HTTPException(status_code=401, detail="Contraseña invalida")
    items =[]
    for data in conn2.read_all():
        dictionary ={}
        dictionary["id"]= data[0]
        dictionary["motivo"]= data[1]
        dictionary["id_recipe"]= data[2]
        dictionary["resuelta"]= data[3]
        items.append(dictionary)
    return template.TemplateResponse("denuncias.html", {"request": req, "items": items})

@app.post("/marcar_resuelta")
def marcar_resuelta(request: Request, denuncia_id: str = Form()):
    conn2.resuelta(denuncia_id)

@app.post("/eliminar_receta")
def eliminar(request: Request, receta_id: str = Form(), denuncia_id: str = Form()):
    conn2.resuelta(denuncia_id)
    conn3.delete(receta_id)

@app.post("/data-processing")
def data_processing(motivo: str = Form(), id_recipe: str = Form()):
  data = {
    "motivo": motivo,
    "id_recipe": id_recipe,
    "resuelta": False,
  }
  conn2.write(data)

@app.get("/api/denuncia/nueva", response_class=HTMLResponse)
def denuncia_nueva(req: Request):
    return template.TemplateResponse("crear_denuncia.html", {"request": req})

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

@app.get("/api/moderadores/{username}")
def get_one(username:str):
    dictionary ={}
    data= conn.get_one(username)
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

"""User Mensajes"""
@app.get("/api/user/messages/sent/{user_id}")
def get_messages_sent(user_id: int):
    allMessages = []
    query = "SELECT m.id, m.emisor_id,m.receptor_id, m.asunto , m.mensaje, m.respuesta , TO_CHAR(m.created_at, 'DD/MM/YYYY HH24:MI') as created_at FROM mensajes as m WHERE m.emisor_id = '{0}' ORDER BY created_at DESC".format(user_id)
    cursor.execute(query)
    for row in cursor.fetchall():
        query_user = "SELECT username from users WHERE id = '{0}'".format(row[2])
        cursor.execute(query_user)
        result = cursor.fetchone()
        json_data = {"id" : row[0] , "emisor_id" : row[1], "receptor_id" : row[2] , "receptor" : result[0] , "asunto" : row[3] , "mensaje" : row[4] , "respuesta" : row[5] , "created_at" : row[6]}
        allMessages.append(json_data)
    return allMessages

@app.get("/api/user/messages/received/{user_id}")
def get_messages_received(user_id: int):
    allMessages = []
    query = "SELECT m.id, m.emisor_id, m.receptor_id, m.asunto, m.mensaje, m.respuesta, TO_CHAR(m.created_at, 'DD/MM/YYYY HH24:MI') as created_at FROM mensajes as m WHERE m.receptor_id = '{0}' ORDER BY created_at DESC".format(user_id)
    cursor.execute(query)
    for row in cursor.fetchall():
        query_user = "SELECT username from users WHERE id = '{0}'".format(row[1])
        cursor.execute(query_user)
        result = cursor.fetchone()
        json_data = {"id" : row[0] , "emisor_id" : row[1] , "emisor" : result[0], "receptor_id" : row[2] , "asunto" : row[3] , "mensaje" : row[4] , "respuesta" : row[5] , "created_at" : row[6]}
        allMessages.append(json_data)
    return allMessages
    

@app.post("/api/user/message/send/{user_id}")
def send_message(user_id , mensaje : SendMessage):
    query = "INSERT INTO mensajes (emisor_id,receptor_id,asunto,mensaje) VALUES('{0}','{1}','{2}','{3}')".format(user_id,mensaje.receptor_id,mensaje.asunto,mensaje.mensaje)
    cursor.execute(query)
    db.commit()
    return {"emisor_id" : user_id , "receptor_id" : mensaje.receptor_id, "asunto": mensaje.asunto, "mensaje" : mensaje.mensaje}

@app.put("/api/user/message/reply/{user_id}")
def reply_message(user_id , mensaje : ReplyMessage):
    query = "UPDATE mensajes set respuesta = '{0}' WHERE id = '{1}' ".format(mensaje.respuesta,mensaje.id)
    cursor.execute(query)
    db.commit()
    return {"id" : mensaje.id , "respuesta" : mensaje.respuesta }


"""Users"""
@app.get("/api/user/{username}")
def get_users(username : str):
    allUsers = []
    query = "SELECT u.id , u.username FROM users as u WHERE username like '{0}%'".format(username)
    cursor.execute(query)
    for row in cursor.fetchall():
        json_data = {"id" : row[0] , "username" : row[1]}
        allUsers.append(json_data)
    return allUsers