async def on_shutdown(app):
    print('shutdown')
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')