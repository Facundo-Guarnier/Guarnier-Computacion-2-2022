import pymongo
from celery_confg import app

"""
    show dbs: Muestra todas las bases de datos disponibles.
    use <database_name>: Cambia a la base de datos especificada.
    show collections: Muestra todas las colecciones de la base de datos actual.
    db.<collection_name>.find(): Muestra todos los documentos de la colección especificada.
    db.<collection_name>.findOne(): Muestra un solo documento de la colección especificada.
    db.<collection_name>.insertOne(<document>): Inserta un solo documento en la colección especificada.
    db.<collection_name>.insertMany(<array_of_documents>): Inserta varios documentos en la colección especificada.
    db.<collection_name>.updateOne(<filter>, <update>): Actualiza un solo documento que cumpla con el filtro especificado.
    db.<collection_name>.updateMany(<filter>, <update>): Actualiza varios documentos que cumplan con el filtro especificado.
    db.<collection_name>.deleteOne(<filter>): Elimina un solo documento que cumpla con el filtro especificado.
    db.<collection_name>.deleteMany(<filter>): Elimina varios documentos que cumplan con el filtro especificado.
"""

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.BatallaNaval
coleccion = db.jugadores



@app.task
def existe_jugador_db(jugador):
    resultado = coleccion.find_one({"nickname":jugador})

    if resultado is not None:     #! Existe el jugador en la BD, no hay que hacer nada. 
        return True
    
    else:           #! No existe el jugador, hay que agregarlo.
        coleccion.insert_one({"nickname":jugador, "ultima_partida":"nada"})
        return False


@app.task
def fin_partida_db(nickname, resultado):
    coleccion.update_one({"nickname":nickname}, {'$set': {"ultima_partida":resultado}})