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
    return {'message': 'Hello World'}


