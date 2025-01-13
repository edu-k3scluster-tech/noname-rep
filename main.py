import multiprocessing
import subprocess
import aiohttp
import os

from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

hello_counter = Counter('hello_counter', documentation='test counter')

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint='/metrics')


@app.get('/')
async def root():
    hello_counter.inc(amount=1)
    return {'service status': "I'm fine"}


@app.get('/test_api_request')
async def test_api_request():
    url = os.getenv('SIMPLE_SERVICE_API')

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return {'message from api': await response.json()}
            return {'error': response.status}


@app.get('/test_secret')
async def test_api_request():
    secret = os.getenv('QWERTY_SECRET')

    return {'secret': secret}


def start_worker():
    subprocess.run(['python', 'worker.py'])


@app.on_event('startup')
async def startup_event():
    worker_process = multiprocessing.Process(target=start_worker)
    worker_process.start()
