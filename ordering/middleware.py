from . import app


@app.middleware('request')
async def inject_oldest_first_url(request):
    request['oldest_first_url'] = None

    if request.url.endswith('/newest_first'):
        request['oldest_first_url'] = '/'.join(request.url.split('/')[:-1])


@app.middleware('request')
async def inject_newest_first(request):
    request['newest_first'] = request.url.endswith('/newest_first')
