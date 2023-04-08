from celery import Celery

app = Celery(
    "Mi Server, conexion y manejo de MongoDB", 
    broker='redis://localhost:6379/0', 
    backend='redis://localhost:6379', 
    include=["celery_task"]
    )   #! Para conectarse a mi docker, mi DB

# app = Celery(
#     "url_celery", 
#     broker='redis://analytics.juncotic.com:6379/0', 
#     backend='redis://analytics.juncotic.com:6379')   #! Para conectarse a la DB del profe.
