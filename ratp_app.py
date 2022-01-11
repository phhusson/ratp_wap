from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.responses import HTMLResponse

import ratp_api
import uvicorn

async def homepage(request):
    lines = ratp_api.lines()
    html = "<html><body>"
    for (lineName, lineId) in lines:
        html += f"<a href=\"stations?line={lineId}\">{lineName}</a><br>"

    html += "</body></html>"

    return HTMLResponse(html)

async def listStations(request):
    lineId = request.query_params['line']
    stations = ratp_api.stationsInLine(lineId)

    html = "<html><body>"
    for (stationName, stationId) in stations:
        html += f"<a href=\"horaires?line={lineId}&station={stationId}\">{stationName}</a><br>"

    html += "</body></html>"
    return HTMLResponse(html)

async def showHoraires(request):
    lineId = request.query_params['line']
    stationId = request.query_params['station']

    missionsA = None
    missionsR = None
    missionsA = ratp_api.nextMissions(lineId, stationId, 'A')
    try:
        missionsA = ratp_api.nextMissions(lineId, stationId, 'A')
    except:
        pass
    try:
        missionsR = ratp_api.nextMissions(lineId, stationId, 'R')
    except:
        pass

    html = "<html><body>"
    if missionsA is not None:
        html += f"Aller vers {missionsA['terminus']}:<br>"
        for (stationDate, stationMessage) in missionsA['missions']:
            hh = stationDate[8:10]
            mm = stationDate[10:12]
            html += f"{hh}:{mm} -- {stationMessage}<br>"
        html += "<br>"
    if missionsR is not None:
        html += f"Retour vers {missionsA['terminus']}:<br>"
        for (stationDate, stationMessage) in missionsR['missions']:
            hh = stationDate[8:10]
            mm = stationDate[10:12]
            html += f"{hh}:{mm} -- {stationMessage}<br>"

    html += "</body></html>"
    return HTMLResponse(html)


app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/stations', listStations),
    Route('/horaires', showHoraires),
])


if __name__ == "__main__":
    uvicorn.run("ratp_app:app", host='127.0.0.1', port=4433, reload = True)
