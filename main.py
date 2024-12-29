import multiprocessing
import subprocess

from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

hello_counter = Counter('hello_counter', documentation='test counter')

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics")


@app.get('/')
async def root():
    hello_counter.inc(amount=1)
    return {'service_status': "I'm fine"}


def start_worker():
    subprocess.run(['python', 'worker.py'])


@app.on_event("startup")
async def startup_event():
    worker_process = multiprocessing.Process(target=start_worker)
    worker_process.start()

