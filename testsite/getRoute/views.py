# Database imports
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.views.generic import ListView, DetailView
from multigtfs.models import *
from django.forms.models import model_to_dict

# Webpage imports
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from getRoute.forms import PostForm
from json import dumps, loads

#calculation tools
from functools import reduce
from os import getcwd
from pyroutelib3 import Router

import math
import geojson as gj
import json
import graph as g

# Create your views here.
from django.views.generic import ListView
from multigtfs.models import (Block, Fare, FareRule, Feed, Frequency, Route,
                              Service, ServiceDate, Shape, ShapePoint, Stop,
                              StopTime, Trip)


# Return List View of Feeds
class ByFeedListView(ListView):
    by_col = 'feed_id'
    by_kwarg = 'feed_id'
    by_class = Feed
    by_classname = 'feed'

    def get_context_data(self, **kwargs):
        context = super(ByFeedListView, self).get_context_data(**kwargs)
        context[self.by_classname] = self.by_class.objects.get(
            id=self.kwargs[self.by_kwarg])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        q_filter = {self.by_col: self.kwargs[self.by_kwarg]}
        qset = super(ByFeedListView, self).get_queryset(**kwargs)
        return qset.filter(**q_filter)


# Return Fare information from Fare List
class FareRuleByFareListView(ListView):
    model = FareRule

    def get_context_data(self, **kwargs):
        context = super(FareRuleByFareListView,
                        self).get_context_data(**kwargs)
        context['fare'] = Fare.objects.get(id=self.kwargs['fare_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return FareRule.objects.filter(fare_id=self.kwargs['fare_id'])


# Return Fare Information from Route List
class FareRuleByRouteListView(ListView):
    model = FareRule

    def get_context_data(self, **kwargs):
        context = super(FareRuleByRouteListView,
                        self).get_context_data(**kwargs)
        context['route'] = Route.objects.get(id=self.kwargs['route_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return FareRule.objects.filter(route_id=self.kwargs['route_id'])


# Return trip Frequency from Trip List View
class FrequencyByTripListView(ListView):
    model = Frequency

    def get_context_data(self, **kwargs):
        context = super(FrequencyByTripListView,
                        self).get_context_data(**kwargs)
        context['trip'] = Trip.objects.get(id=self.kwargs['trip_id'])
        return context

    def get_queryset(self, **kwargs):
        return Frequency.objects.filter(trip=self.kwargs['trip_id'])


# Returns Service Date from Service List
class ServiceDateByServiceListView(ListView):
    model = ServiceDate

    def get_context_data(self, **kwargs):
        context = super(ServiceDateByServiceListView,
                        self).get_context_data(**kwargs)
        context['service'] = Service.objects.get(id=self.kwargs['service_id'])
        return context

    def get_queryset(self, **kwargs):
        return ServiceDate.objects.filter(service=self.kwargs['service_id'])


# Returns Shape Point from Shape List
class ShapePointByShapeListView(ListView):
    model = ShapePoint

    def get_context_data(self, **kwargs):
        context = super(ShapePointByShapeListView,
                        self).get_context_data(**kwargs)
        context['shape'] = Shape.objects.get(id=self.kwargs['shape_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return ShapePoint.objects.filter(shape=self.kwargs['shape_id'])


# Returns Stop Time from Stop List
class StopTimeByStopListView(ListView):
    model = StopTime

    def get_context_data(self, **kwargs):
        context = super(StopTimeByStopListView,
                        self).get_context_data(**kwargs)
        context['stop'] = Stop.objects.get(id=self.kwargs['stop_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return StopTime.objects.filter(stop_id=self.kwargs['stop_id'])


# Returns Stop Time from Trip List
class StopTimeByTripListView(ListView):
    model = StopTime

    def get_context_data(self, **kwargs):
        context = super(StopTimeByTripListView,
                        self).get_context_data(**kwargs)
        context['trip'] = Trip.objects.get(id=self.kwargs['trip_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return StopTime.objects.filter(trip=self.kwargs['trip_id'])


# Refurns Trip from Block List
class TripByBlockListView(ListView):
    model = Trip

    def get_context_data(self, **kwargs):
        context = super(TripByBlockListView, self).get_context_data(**kwargs)
        context['the_block'] = Block.objects.get(id=self.kwargs['block_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(block_id=self.kwargs['block_id'])


# Returns Trip from Route List
class TripByRouteListView(ListView):
    model = Trip

    def get_context_data(self, **kwargs):
        context = super(TripByRouteListView, self).get_context_data(**kwargs)
        context['route'] = Route.objects.get(id=self.kwargs['route_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(route_id=self.kwargs['route_id'])


# Returns Trip from Service List
class TripByServiceListView(ListView):
    model = Trip

    def get_context_data(self, **kwargs):
        context = super(TripByServiceListView, self).get_context_data(**kwargs)
        context['service'] = Service.objects.get(id=self.kwargs['service_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(service=self.kwargs['service_id'])


# Returns Trip from Shape List
class TripByShapeListView(ListView):
    model = ShapePoint

    def get_context_data(self, **kwargs):
        context = super(TripByShapeListView, self).get_context_data(**kwargs)
        context['shape'] = Shape.objects.get(id=self.kwargs['shape_id'])
        context['feed_id'] = self.kwargs['feed_id']
        return context

    def get_queryset(self, **kwargs):
        return Trip.objects.filter(shape=self.kwargs['shape_id'])


class getDefaultMap(object):
    def index_map(request):
        if request.POST:
            print('asdf')
            # return render('default.html',RequestContext(request))

        CORK_COORDINATES = (51.8983, -8.4726)

        context = {}
        return render(request, 'default.html', context)


class ContainedPoints(object):
    def test(request):
        if request.method == 'POST':
            response_data = {}

            def makeGeomStr(geom):
                # Format latitude and longitude
                geom = geom.translate({ord(i): None
                                       for i in '\{\}[]'}).split(',')
                geom = [i[6:] for i in geom]

                # Create POLYGON geometry string
                geomString = ''
                geomClosePoint = geom[1] + ' ' + geom[0]
                geomString += geomClosePoint
                # First and last coordinate must match
                for i in range(2, len(geom) - 1, 2):
                    point = ',' + str(geom[i + 1]) + ' ' + str(geom[i])
                    geomString += point
                geomString += ',' + geomClosePoint
                queryGeom = '%s((%s))' % (shape, geomString)
                print(queryGeom)
                return queryGeom

            def getData(table):
                # Can instead SELECT x FROM x where contains is true for imporved performance
                cursor = connection.cursor()

                if table == 'stop':
                    # Find all stops inside the polygon
                    # SELECT ST_CONTAINS(ST_GEOMFROMTEXT('SRID=4326;POLYGON((-9.232910089194776 55.677584411089526 ,-11.307128705084326 50.83647280350753,-4.5219720527529725 50.58044602533059,-4.9614251777529725 55.3591315224922,-9.232910089194776 55.677584411089526))'), shape_point.point), shape_point.point FROM shape_point ;
                    # SELECT ST_Contains(ST_GEOMFROMTEXT('SRID=4326;POLYGON((52.36620837113711 -9.263671925291419,52.204913551431154 -7.562988130375745,51.54291871811506 -7.993652326986195,51.646657472959326 -9.303222605958581,  52.36620837113711 -9.263671925291419))'), stop.point) , stop.point FROM stop ;
                    # SELECT ST_Contains(ST_GEOMFROMTEXT('SRID=4326;POLYGON((-9.263671925291419 52.36620837113711,-7.562988130375745 52.204913551431154,-7.993652326986195 51.54291871811506,-9.303222605958581 51.646657472959326,-9.263671925291419 52.36620837113711))'), stop.point)  , stop.point FROM stop ;

                    query = "SELECT stop.name, (ST_AsText(stop.point)), stop_id FROM %s WHERE ST_Contains(ST_GeomFromText('SRID=4326;%s'), stop.point)" % (
                        table, queryGeom)
                    # query = "SELECT ST_Contains(ST_GeomFromText('SRID=4326;%s'), point), name , ST_X(point), ST_Y(point) FROM %s;"%(queryGeom, table)
                    cursor.execute(query)

                    # Get all Stops
                    stops = cursor.fetchall()
                    # stops =  [(x,y,n) for i,n,x,y in list(filter(lambda x: x[0] == True, stops))]

                    return stops
                # Must Return only the points IN the polygon not all shapes
                elif table == 'shape':
                    # Find all shapes inside polygon

                    # SELECT shape_id FROM shape WHERE ST_Contains(ST_GeomFromText('SRID=4326;POLYGON((-9.263671925291419 52.36620837113711,-7.562988130375745 52.204913551431154,-7.993652326986195 51.54291871811506,-9.303222605958581 51.646657472959326,-9.263671925291419 52.36620837113711))'), shape.geometry) ;

                    query = "SELECT shape_id, (ST_AsText(shape.geometry)) FROM %s WHERE ST_Intersects(ST_GeomFromText('SRID=4326;%s'), shape.geometry)" % (
                        table, queryGeom)
                    # query = "SELECT shape_id, (ST_AsGEOJSON(shape.geometry)) FROM %s WHERE ST_Intersects(ST_GeomFromText('SRID=4326;%s'), shape.geometry)"%(table, queryGeom)
                    cursor.execute(query)

                    shapes = cursor.fetchall()
                    # print(shapes)
                    return shapes

                elif table == 'trip':
                    # Find all trips inside polygon
                    query = "SELECT DISTINCT headsign,(ST_AsText(trip.geometry)) FROM %s WHERE ST_Intersects(ST_GeomFromEWKT('SRID=4326;%s'), trip.geometry)" % (
                        table, queryGeom)
                    cursor.execute(query)

                    trips = cursor.fetchall()

                    return trips

                elif table == 'route':
                    # to implement routes
                    pass

            # Get shape and geom data
            shape = request.POST.get('type')
            geom = request.POST.get('latlng')
            toFind = request.POST.get('toFind')

            queryGeom = makeGeomStr(geom)
            data = getData(toFind)
            # Find all stops within polygon bounds

            response_data['shape'] = shape
            response_data['toFind'] = toFind
            response_data['geom'] = data
            response_data['count'] = len(data)

            return HttpResponse(dumps(response_data),
                                content_type="application/json")

        else:
            return HttpResponse(dumps(
                {"nothing to see": "this isn't happening"}),
                                content_type="application/json")

        return render(request, 'default.html', {})


class Path(object):
    def shortestPath(request):
        if request.method == 'POST':
            response_data = {}

            alat = request.POST.get('alat')  # end/destination
            alon = request.POST.get('alon')  # end/destination
            blat = request.POST.get('blat')  # start/source
            blon = request.POST.get('blon')  # start/source
            mode = request.POST.get('mode')  # start/source

            # Initialise Router Object
            router = Router(mode)

            # Find start and end nodes
            try:
                start = router.findNode(float(alat), float(alon))
                end = router.findNode(float(blat), float(blon))
            except ValueError:
                return render(request, 'default.html', {})

            # Find the route - a list of OSM nodes and return status
            status, route = router.doRoute(start, end)

            if status == 'success':
                dist = 0
                avgspeeds = {
                    'foot': 1.4,
                    'cycle': 5.55556,
                    'car': 13.8889,
                }

                geom = list(map(router.nodeLatLon,
                                route))  # Get actual route coordinates

                # Calculate distance of path with haversine formula (Slightly off)
                i = 0
                while i < len(geom) - 1:
                    dist += router.distance(geom[i], geom[i + 1])
                    i += 1

                avgtime = round(((dist * 1000) / avgspeeds[mode]) / 60,
                                3)  # Average walking speed 1.4km
                dist = round(dist, 3)  # Convert to km

            # elif status == 'noroute':
            #     pass
            # elif status == 'gaveup':
            #     pass

            else:
                # some error
                geom = []

            # Work with graph data to get shortest path
            response_data['shape'] = 'Shortest Route'
            response_data['geom'] = geom
            response_data['count'] = len(geom)
            response_data['source'] = (alat, alon)
            response_data['destination'] = (blat, blon)
            response_data['duration'] = avgtime
            response_data['distance'] = dist

            return HttpResponse(dumps(response_data),
                                content_type="application/json")

        else:
            return HttpResponse(dumps(
                {"nothing to see": "this isn't happening"}),
                                content_type="application/json")

        return render(request, 'default.html', {})

    def shortestGTFSPath(request):
        if request.method == 'POST':

            alat = request.POST.get('alat')  # end/destination
            alon = request.POST.get('alon')  # end/destination
            blat = request.POST.get('blat')  # start/source
            blon = request.POST.get('blon')  # start/source

            try:
                alat = float(alat)
                alon = float(alon)
                blat = float(blat)
                blon = float(blon)

            except ValueError:
                return render(request, 'default.html', {})

            response_data = {}

            cursor = connection.cursor()

            query = 'SELECT stop.id, stop.stop_id, ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) ORDER BY dist;' % (
                alon, alat, alon, alat, 1000 / 149838.673031)
            cursor.execute(query)
            astops = cursor.fetchall()

            query = 'SELECT stop.id, stop.stop_id, ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) ORDER BY dist;' % (
                blon, blat, blon, blat, 1000 / 149838.673031)
            cursor.execute(query)
            bstops = cursor.fetchall()

            # Reads in every stop in ireland and is not necessary
            graph = g.DijkstraShortestPath.PathFinder()
            graph.buildFromDB(connection)

            # TO FIND APROPRIATE VERTICES
            shortest = [1000000, None, None, None]
            for start in astops:
                allPaths = graph(start[0])
                v = graph._graph.getVertexByLabel(start[0])
                for end in bstops:
                    w = graph._graph.getVertexByLabel(end[0])

                    weight, prev = allPaths[w]
                    totaldist = weight + (start[2] +
                                          end[2]) * 149838.673031 * 2

                    if totaldist < shortest[0]:
                        shortest[0] = totaldist
                        shortest[1] = v
                        shortest[2] = w
                        shortest[3] = allPaths

            # Finds the route name from all the stops in the path
            # Does not factor in transfers
            # WITH path AS(SELECT * FROM stop WHERE id = '2093' OR id = '2232' OR id = '2320' OR id = '2090') SELECT DISTINCT route.short_name FROM stop_time INNER JOIN path ON path.id = stop_time.stop_id INNER JOIN trip ON trip.id = stop_time.trip_id INNER JOIN route ON route.id = trip.route_id;

            # allPaths = graph(int(shortest[1].element()))
            print(shortest[1], shortest[2])
            path = graph.shortestPath(shortest[1], shortest[2], shortest[3])
            routes = []

            # for i in range(len(path)-1, 1, -1):
            #     print(i)
            #     nodea = path[i][2]
            #     nodeb = path[i-1][2]
            #     for edge in graph._graph.edges():
            #         # print(edge)
            #         vertices = edge._vertices
            #         print(vertices[0].element())
            #         print(vertices[1].element())
            #         print(nodea, nodeb)
            #         if vertices[0].element() == nodea and vertices[1].element() == nodeb:
            #             if edge._name not in routes:
            #                 routes.append(edge._name)
            #     break
            # for i in range(len(path)-1, 0, -1):
            #     A = graph._graph.getVertexByLabel(int(path[i][2]))
            #     B = graph._graph.getVertexByLabel(int(path[i-1][2]))
            #     route = graph._graph._inedges[B][A]._name
            #     print(route)
            #     if route not in routes:
            #         routes.append(route)
            # print(routes)

            response_data['path'] = path

            return HttpResponse(dumps(response_data),
                                content_type="application/json")

        else:
            return HttpResponse(dumps(
                {"nothing to see": "this isn't happening"}),
                                content_type="application/json")

        return render(request, 'default.html', {})

    def nearGTFSRoutes(request):
        if request.method == 'POST':
            response_data = {}

            alat = request.POST.get('alat')  # end/destination
            alon = request.POST.get('alon')  # end/destination
            blat = request.POST.get('blat')  # start/source
            blon = request.POST.get('blon')  # start/source
            mode = request.POST.get('mode')

            modes = {'bus': '1', 'tram': '2'}

            # Should have try except catch
            # Should have in database
            with open('route_shapes1.geojson') as file:
                allLines = json.load(file)['features']
                routes = []
                cursor = connection.cursor()
                for line in allLines:
                    route = str(line['geometry']).replace('\'', '\"')
                    routeid = line['properties']['route_id']

                    query = 'SELECT route.short_name FROM route where route_id= \'%s\' AND ST_DWITHIN(ST_SetSRID(ST_GeomFromGeoJSON(\'%s\'), 4326), ST_SetSRID(ST_MakePoint(%s, %s), 4326), 0.006) AND ST_DWITHIN(ST_SetSRID(ST_GeomFromGeoJSON(\'%s\'), 4326), ST_SetSRID(ST_MakePoint(%s, %s), 4326), 0.006) AND feed_id = \'%s\';' % (
                        routeid, route, alat, alon, route, blat, blon,
                        modes[mode])
                    cursor.execute(query)
                    routeShortName = cursor.fetchall()
                    routeShortName
                    if routeShortName:
                        line['properties'][
                            'route_short_name'] = routeShortName[0][0]
                        routes.append(line)

            response_data['trips'] = routes
            return HttpResponse(dumps(response_data),
                                content_type="application/json")

        else:
            return HttpResponse(dumps(
                {"nothing to see": "this isn't happening"}),
                                content_type="application/json")

        return render(request, 'default.html', {'form': form})

    def nearGTFSStops(request):
        if request.method == 'POST':

            response_data = {}

            alat = request.POST.get('alat')  # end/destination
            alon = request.POST.get('alon')  # end/destination
            blat = request.POST.get('blat')  # start/source
            blon = request.POST.get('blon')  # start/source
            mode = request.POST.get('mode')
            radius = request.POST.get('radius')

            if not radius:
                radius = 1

            radius = float(radius) * 1000
            # Get Feed ID of the mode
            modes = {
                'bus': '1',
                'tram': '2',
                'dijk': '3',
            }
            if modes[mode] == '3':
                graph = g.DijkstraShortestPath.PathFinder()
                graph.buildFromDB(connection)

                startLabel = '1bb1'
                allpaths = graph(startLabel)

                cursor = connection.cursor()
                query = 'SELECT stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist, stop.stop_id, stop.id FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) AND feed_id = \'%s\' ORDER BY dist;' % (
                    -8.475218, 51.897479, -8.475218, 51.897479,
                    10000 / 149838.673031, 1)
                cursor.execute(query)

                allstops = cursor.fetchall()
                allpoints = {}

                for i in allstops:
                    try:
                        allpoints[i[5]] = graph.shortestPath(
                            '1bb1', i[5], allpaths)
                        # print(i)
                    except KeyError:
                        print('Key Error -> ', i)

                # print(allpoints)
                nodes = {}
                output = []
                with open('togherNodes.txt') as togher:
                    line = togher.readline()
                    line = togher.readline().strip().split(',')
                    pid = line[0]
                    longitude = line[1]
                    latitude = line[2]
                    weight = 0
                    query = 'SELECT stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist, stop.stop_id, stop.id FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) AND feed_id = \'%s\' ORDER BY dist;' % (
                        longitude, latitude, longitude, latitude,
                        100 / 149838.673031, 1)
                    cursor.execute(query)
                    nearstops = cursor.fetchall()
                    # print(nearstops)
                    # print('-------')
                    for i in nearstops:
                        stopid = i[5]
                        distance = i[3]*149838.673031
                        try:
                            tempweight = distance + graph.shortestPath(
                                '1bb1', i[5], allpaths)[0][3]
                        except KeyError:
                            tempweight = 0

                    weight += tempweight
                    nodes[pid] = [latitude, longitude, weight]

                    while line[0]:
                        line = togher.readline().strip().split(',')
                        if not line[0]:
                            break
                        else:
                            pid = line[0]
                            longitude = line[1]
                            latitude = line[2]
                            weight = 0

                            query = 'SELECT stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist, stop.stop_id, stop.id FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) AND feed_id = \'%s\' ORDER BY dist;' % (
                                longitude, latitude, longitude, latitude,
                                1000 / 149838.673031, 1)
                            cursor.execute(query)
                            nearstops = cursor.fetchall()
                            # print(nearstops)
                            # print('-------')
                            for i in nearstops:
                                stopid = i[5]
                                distance = i[3]*149838.673031
                                # print(distance)
                                try:
                                    tempweight = distance + graph.shortestPath(
                                        '1bb1', i[5], allpaths)[0][3]
                                except KeyError:
                                    tempweight = 0

                            weight += tempweight
                            nodes[pid] = [float(latitude), float(longitude), weight]
                            output.append(['temp',float(latitude), float(longitude) ,None, None, None,weight])
                # print(nodes)
                # print(output)
                response_data['astops'] = output
                response_data['bstops'] = []

            elif modes[mode] == '2':
                with open('stopsLightRail.txt') as file:
                    line = file.readline()
                    astops = []
                    bstops = []

                    line = file.readline().split(',')
                    number = 1
                    line[-1] = line[-1].strip()
                    # line.append(number)
                    temp = [
                        line[1],
                        float(line[2]),
                        float(line[3]), 0, line[0], number, 1728
                    ]  # 288
                    astops.append(temp)
                    while line[0]:
                        line = file.readline().split(',')
                        if not line[0]:
                            break
                        number += 1
                        line[-1] = line[-1].strip()
                        temp = [
                            line[1],
                            float(line[2]),
                            float(line[3]), 0, line[0], number, 1728
                        ]
                        astops.append(temp)
                        bstops.append(temp)

                    # print(astops)
                    # print('--------------')
                    response_data['astops'] = astops
                    response_data['bstops'] = bstops

                
            
            # Get the n nearest stops within 1 km
            else:
                query = 'WITH tripcount AS (SELECT stop.id, COUNT(route.id) as a FROM stop_time INNER JOIN stop on stop_time.stop_id = stop.id INNER JOIN trip ON stop_time.trip_id = trip.id INNER JOIN route ON trip.route_id = route.id GROUP BY stop.id) SELECT stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist, stop.stop_id, stop.id, tripcount.a FROM stop INNER JOIN tripcount ON tripcount.id = stop.id WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) AND feed_id = \'%s\' ORDER BY dist;' % (
                    alon, alat, alon, alat,
                    (radius) / 149838.673031, modes[mode])
                cursor = connection.cursor()

                cursor.execute(query)
                astops = cursor.fetchall()
                # print(astops)

                query = 'WITH tripcount AS (SELECT stop.id, COUNT(route.id) as a FROM stop_time INNER JOIN stop on stop_time.stop_id = stop.id INNER JOIN trip ON stop_time.trip_id = trip.id INNER JOIN route ON trip.route_id = route.id GROUP BY stop.id) SELECT stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist, stop.stop_id, stop.id, tripcount.a FROM stop INNER JOIN tripcount ON tripcount.id = stop.id WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) AND feed_id = \'%s\' ORDER BY dist;' % (
                    blon, blat, blon, blat,
                    (radius) / 149838.673031, modes[mode])
                cursor.execute(query)
                bstops = cursor.fetchall()

                response_data['astops'] = astops
                # for i in astops:
                    # print(i[5])
                response_data['bstops'] = bstops


            return HttpResponse(dumps(response_data),
                                content_type="application/json")

        else:
            return HttpResponse(dumps(
                {"nothing to see": "this isn't happening"}),
                                content_type="application/json")

        return render(request, 'default.html', {})

    def coverage(request):
        if request.method == 'POST':

            response_data = {}

            print('Calculating Coverage')
            graph = g.DijkstraShortestPath.PathFinder()
            graph.buildFromDB(connection)

            startLabel = '1bb1'
            allpaths = graph(startLabel)

            cursor = connection.cursor()
            query = 'SELECT stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist, stop.stop_id, stop.id FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) AND feed_id = \'%s\' ORDER BY dist;' % (
                -8.475218, 51.897479, -8.475218, 51.897479,
                10000 / 149838.673031, 1)
            cursor.execute(query)

            allstops = cursor.fetchall()
            allpoints = {}

            for i in allstops:
                try:
                    allpoints[i[5]] = graph.shortestPath(
                        '1bb1', i[5], allpaths)
                    # print(i)
                except KeyError:
                    print('Key Error -> ', i)

            # print(allpoints)
            nodes = {}
            output = []
            with open('outfile.txt') as togher:
                maxVal = -10000000
                minVal = 10000000
                line = togher.readline()
                line = togher.readline().strip().split(',')
                pid = line[0]
                longitude = line[1]
                latitude = line[2]
                weight = 0
                query = 'SELECT stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist, stop.stop_id, stop.id FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) AND feed_id = \'%s\' ORDER BY dist;' % (
                    longitude, latitude, longitude, latitude,
                    1000 / 149838.673031, 1)
                cursor.execute(query)
                nearstops = cursor.fetchall()
                # print(nearstops)
                # print('-------')
                for i in nearstops:
                    stopid = i[5]
                    distance = i[3]*149838.673031
                    tempweight = 0
                    try:
                        tempweight = distance + graph.shortestPath(
                            '1bb1', i[5], allpaths)[0][3]
                    except KeyError:
                        tempweight = 0

                weight += tempweight
                nodes[pid] = [latitude, longitude, weight]

                while line[0]:
                    line = togher.readline().strip().split(',')
                    if not line[0]:
                        break
                    else:
                        pid = line[0]
                        longitude = line[1]
                        latitude = line[2]
                        weight = 0

                        query = 'SELECT stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist, stop.stop_id, stop.id FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), %f)) AND feed_id = \'%s\' ORDER BY dist;' % (
                            longitude, latitude, longitude, latitude,
                            1000 / 149838.673031, 1)
                        cursor.execute(query)
                        nearstops = cursor.fetchall()
                        # print(nearstops)
                        # print('-------')
                        for i in nearstops:
                            stopid = i[5]
                            distance = i[3]*149838.673031
                            # print(distance)
                            try:
                                tempweight = distance + graph.shortestPath(
                                    '1bb1', i[5], allpaths)[0][3]
                            except KeyError:
                                tempweight = 0

                        weight += tempweight
                        if weight > maxVal:
                            maxVal = weight
                        elif weight < minVal and weight > 0:
                            minVal = weight
                        nodes[pid] = [float(latitude), float(longitude), weight]
                        output.append(['temp',float(latitude), float(longitude) ,None, None, None,float(weight)])

            # print(nodes)
            print(output)
            print(minVal, maxVal)
            response_data['astops'] = output
            response_data['bstops'] = []


            return HttpResponse(dumps(response_data),
                        content_type="application/json")

        else:
            return HttpResponse(dumps(
                {"nothing to see": "this isn't happening"}),
                                content_type="application/json")

        return render(request, 'default.html', {})


    # SELECT stop_time.id, stop_time.shape_dist_traveled, stop_time.arrival_time, stop_time.departure_time, stop_time.stop_sequence, stop_time.stop_id, trip.trip_id, trip.shape_id FROM stop_time INNER JOIN trip ON trip.trip_id::text LIKE CONCAT(stop_time.trip_id, '%') WHERE ST_INTERSECTS();

    # WITH alltrips AS (SELECT trip_id, (ST_AsText(trip.geometry)) FROM trip WHERE ST_Intersects(ST_GeomFromEWKT('SRID=4326;POLYGON((-8.491573327191873 51.899935131979994,-8.507137298147429 51.891601878352944,-8.499584194942146 51.88712858619483,-8.48356246468029 51.88844707836375,-8.47913742225501 51.89216689307324,-8.486919401184425 51.89889944503624,-8.491573327191873 51.899935131979994))'), trip.geometry)) SELECT stop_time.id, stop_time.shape_dist_traveled, stop_time.arrival_time, stop_time.departure_time, stop_time.stop_sequence, stop_time.stop_id, alltrips.alltrips.id, alltrips.shape_id FROM stop_time INNER JOIN alltrips.ON alltrips.alltrips.id::text LIKE CONCAT(stop_time.alltrips.id, '%') limit 10;

    # Get all stop times joined with trips
    # WITH alltrips AS (SELECT trip_id, shape_id ,(ST_AsText(trip.geometry)) FROM trip WHERE ST_Intersects(ST_GeomFromEWKT('SRID=4326;POLYGON((-8.491573327191873 51.899935131979994,-8.507137298147429 51.891601878352944,-8.499584194942146 51.88712858619483,-8.48356246468029 51.88844707836375,-8.47913742225501 51.89216689307324,-8.486919401184425 51.89889944503624,-8.491573327191873 51.899935131979994))'), trip.geometry)) SELECT stop_time.id, stop_time.shape_dist_traveled, stop_time.arrival_time, stop_time.departure_time, stop_time.stop_sequence, stop_time.stop_id, alltrips.trip_id, alltrips.shape_id FROM stop_time INNER JOIN alltrips ON alltrips.trip_id::text LIKE CONCAT(stop_time.id, '%') WHERE alltrips.trip_id = '4405.y1008.10-80-e16-1.24.I';

    # WITH start AS (SELECT stop.stop_id, stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(-8.502101898629919, 51.88897681594591), 4326)) AS dist FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(-8.502101898629919, 51.88897681594591), 4326), 20)) ORDER BY dist limit 5) WITH end AS (SELECT stop.stop_id, stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(-8.48371505722753, 51.893967831801525), 4326)) AS dist FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(-8.48371505722753, 51.893967831801525 ), 4326), 20)) ORDER BY dist limit 5) WITH alltrips AS (SELECT trip_id, shape_id ,(ST_AsText(trip.geometry)) FROM trip WHERE ST_Intersects(ST_GeomFromEWKT('SRID=4326;POLYGON((-8.491573327191873 51.899935131979994,-8.507137298147429 51.891601878352944,-8.499584194942146 51.88712858619483,-8.48356246468029 51.88844707836375,-8.47913742225501 51.89216689307324,-8.486919401184425 51.89889944503624,-8.491573327191873 51.899935131979994))'), trip.geometry))
    # WITH alltrips AS (SELECT trip_id, shape_id ,(ST_AsText(trip.geometry)) FROM trip WHERE ST_Intersects(ST_GeomFromEWKT('SRID=4326;POLYGON((-8.491573327191873 51.899935131979994,-8.507137298147429 51.891601878352944,-8.499584194942146 51.88712858619483,-8.48356246468029 51.88844707836375,-8.47913742225501 51.89216689307324,-8.486919401184425 51.89889944503624,-8.491573327191873 51.899935131979994))'), trip.geometry)) SELECT stop_time.id, stop_time.shape_dist_traveled, stop_time.arrival_time, stop_time.departure_time, stop_time.stop_sequence, stop_time.stop_id, alltrips.trip_id, alltrips.shape_id FROM stop_time INNER JOIN alltrips ON alltrips.trip_id::text LIKE CONCAT(stop_time.trip_id, '%') WHERE alltrips.trip_id = '4405.y1008.10-80-e16-1.24.I';

    # Get all stops within 1 km of a point
    # SELECT stop_id, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(-8.484096528118245, 51.90451305689584 ), 4326)) AS dist FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(-8.484096528118245, 51.90451305689584 ), 4326), 1)) ORDER BY dist limit 5;

    #WITH stopinfo as (SELECT stop.id, stop_time.arrival_time, stop_time.departure_time, stop_time.stop_sequence,stop.stop_id, stop.point, trip.trip_id FROM stop_time INNER JOIN stop ON stop.id = stop_time.stop_id INNER JOIN trip ON trip.trip_id::text LIKE CONCAT(stop_time.trip_id, '%') ) SELECT stopinfo.stop_id, ST_X(stopinfo.point), ST_Y(stopinfo.point), stopinfo.trip_id, ST_Distance(stopinfo.point, ST_SetSRID(ST_MakePoint(-8.484096528118245, 51.90451305689584 ), 4326)) AS dist FROM stopinfo WHERE ST_Intersects(stopinfo.point, ST_Buffer(ST_SetSRID(ST_MakePoint(-8.484096528118245, 51.90451305689584 ), 4326), 0.5)) limit 1;

    # WITH start AS (SELECT stop.id, stop.stop_id, stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(-8.502101898629919, 51.88897681594591), 4326)) AS dist FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(-8.502101898629919, 51.88897681594591), 4326), 1)) ORDER BY dist) SELECT stop_time.id, stop_time.shape_dist_traveled, stop_time.arrival_time, stop_time.departure_time, stop_time.stop_sequence, stop_time.stop_id, trip.trip_id, trip.shape_id , stop.stop_id ,ST_X(stop.point), ST_Y(stop.point) FROM stop_time INNER JOIN trip ON trip.trip_id::text LIKE CONCAT(stop_time.trip_id, '%') INNER JOIN stop ON stop.id = stop_time.id INNER JOIN start ON start.id = stop_time.id limit 50;
    # SELECT trip_id, ST_AsTEXT(trip.geometry) FROM trip WHERE ST_Intersects(trip.geometry, ST_Buffer(ST_SetSRID(ST_MakePoint(-8.48907297416191, 51.8935714442932), 4326), 100/149838.673031));
    # SELECT trip_id, ST_AsTEXT(trip.geometry) FROM trip WHERE ST_Intersects(trip.geometry, ST_Buffer(ST_SetSRID(ST_MakePoint(-8.5017517466627, 51.8892032418095), 4326), 100/149838.673031));
    # WITH start AS (SELECT stop.id, stop.stop_id, stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(-8.50166608632273, 51.8893384454823), 4326)) AS dist FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(-8.50166608632273, 51.8893384454823), 4326), 149838.673031)) ORDER BY dist) SELECT stop.*, stop_time.*, trip.trip_id FROM stop INNER JOIN stop_time ON stop_time.stop_id = stop.id INNER JOIN trip ON trip.trip_id::text LIKE CONCAT(stop_time.trip_id, '%') INNER JOIN start ON start.stop_id = stop.stop_id ORDER BY stop_time.id limit 10;
    # SELECT stop.name, ST_Y(stop.point) ,ST_X(stop.point),ST_Distance(stop.point, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS dist, stop_id FROM stop WHERE ST_Intersects(stop.point, ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326), )) ORDER BY dist;
