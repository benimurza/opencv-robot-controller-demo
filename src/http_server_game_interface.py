from aiohttp import web

from gamewebinterface import GameInterfaceCar


async def handle(request):
    gic = GameInterfaceCar()
    return web.Response(text=gic.to_json().replace("'", "\""))

app = web.Application()
app.router.add_get('/cars', handle)

web.run_app(app)