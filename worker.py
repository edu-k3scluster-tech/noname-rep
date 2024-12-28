import argparse
import asyncio
import uvicorn

from typing import Annotated

from fastapi import FastAPI, Depends
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

hello_counter = Counter('hello_counter', documentation='test counter')

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint='/metrics')


class Worker:
    def __init__(self):
        self._status = "I'm fine"

    async def run(self):
        while True:
            await asyncio.sleep(10)

    async def get_status(self):
        return self._status


worker = Worker()


async def startup_event():
    asyncio.create_task(worker.run())

app.add_event_handler('startup', startup_event)


@app.get('/worker')
async def root(worker_status: Annotated[str, Depends(worker.get_status)]):
    hello_counter.inc(amount=1)
    return {'worker_status': worker_status}


def get_args():
    parser = argparse.ArgumentParser(description='worker')
    parser.add_argument(
        '--port', type=int, default=8000, help="worker port"
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    uvicorn.run(app, host='0.0.0.0', port=args.port)


