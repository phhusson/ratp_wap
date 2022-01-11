#!/usr/bin/env python3

import zeep
from zeep.plugins import HistoryPlugin
from dataclasses import dataclass

zeepHistory = HistoryPlugin()
client = zeep.Client(wsdl = 'Wsiv.wsdl', plugins=[zeepHistory])
stationType = client.get_type('ns0:Station')
lineType = client.get_type('ns0:Line')
directionType = client.get_type('ns0:Direction')

#hiddenLines = [
#        'RA', 'RB',
#        'M1', 'M2', 'M3', 'M3B', 'M4', 'M5', 'M6', 'M7', 'M7B', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M14',
#        'BT1', 'BT2', 'BT3a', 'BT3b', 'BT5', 'BT6', 'BT7', 'BT8',
#        'B38', 'B197',
#        'BN01', 'BN02', 'BN14', 'BN11', 'BN22', 'BN23', 'BN24', 'BN122'
#]
hiddenLines = None
def lines():
    global hiddenLines
    if hiddenLines is not None:
        return hiddenLines

    rawLines = client.service.getLines()
    allReseau = set([x['reseau']['name'] for x in rawLines])
    lines = [ (x['reseau']['name'] + ' ' + x['code'] + ': '+ x['name'], x['codeStif']) for x in rawLines ]

    # This is called hiddenLines, because those codes doesn't appear in getLines
    # The code given in getLines doesn't give us actual station display
    hiddenLines = [ (x['reseau']['name'] + ' ' + x['code'] + ': '+ x['name'], 'R' + x['code']) for x in rawLines if x['reseau']['name'] == 'RER' ]
    hiddenLines += [ (x['reseau']['name'] + ' ' + x['code'] + ': '+ x['name'], 'M' + x['code']) for x in rawLines if x['reseau']['name'] == 'Métro' ]
    # code contains prefixing T
    hiddenLines += [ (x['reseau']['name'] + ' ' + x['code'] + ': '+ x['name'], 'B' + x['code']) for x in rawLines if x['reseau']['name'] == 'Tramway' ]
    hiddenLines += [ (x['reseau']['name'] + ' ' + x['code'] + ': '+ x['name'], 'B' + x['code']) for x in rawLines if x['reseau']['name'] == 'Bus RATP' ]
    # code contains prefixing N
    hiddenLines += [ (x['reseau']['name'] + ' ' + x['code'] + ': '+ x['name'], 'B' + x['code']) for x in rawLines if x['reseau']['name'] == 'Noctilien' ]
    # Missing: SNCF, Bus OPTILE

    return hiddenLines

def stationsInLine(lineId):
    line = lineType(id=lineId)
    stationsInLine = stationType(line=line)
    stations = client.service.getStations(station = stationsInLine)

    return [
            (x.name, x['id'])
                for x in stations.stations]

def nextMissions(lineid, stationId, sens):
    line = lineType(id=lineid)
    station = stationType(id=stationId, line=line)
    direction = directionType(sens=sens)
    missionsNext = client.service.getMissionsNext(station, direction = direction)

    missions = [
            (x.stationsDates[0] if len(x.stationsDates)>0 else '', x.stationsMessages[0])
            for x in missionsNext.missions]

    return {
            'terminus': missionsNext.argumentDirection.name,
            'missions': missions }

#stations = stationsInLine('M4')
#print(stations)
#
#mis = nextMissions('M4', '213', 'A')
#print(mis)
