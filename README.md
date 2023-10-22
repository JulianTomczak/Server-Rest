## Instalacion

- [Instalar Python](https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe)
- `python -m pip install --upgrade pip` (puede ser que en vez de python sea py o python3)
- `git clone https://github.com/MauroLucas/server-rest.git` (Es posible que tengas que pedir acceso a Mauro)
- `cd .\server-rest\`
- `pip3 install virtualenv` 
- `virtualenv venv` (Crear el entorno virtual)
- `Set-ExecutionPolicy -Scope LocalMachine unrestricted` (Usando powershell)
- `./venv/scripts/activate`
- `pip install -r requirements.txt`
- `uvicorn main:app --reload`(http://127.0.0.1:8000/docs para acceder al swagger)




