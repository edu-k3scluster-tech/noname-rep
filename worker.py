import asyncio


class Worker:
    async def run(self):
        while True:
            await asyncio.sleep(10)


worker = Worker()


if __name__ == '__main__':
    asyncio.run(worker.run())


