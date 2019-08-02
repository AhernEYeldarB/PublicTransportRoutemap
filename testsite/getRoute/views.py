# Database imports
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.views.generic import ListView, DetailView
from multigtfs.models import *

# Wepage imports
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from getRoute.forms import PostForm
from json import dumps, loads

from functools import reduce
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


# class AllRoutesInPolygon(ListVIew):
#     model =


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
                geom = geom.translate({ord(i): None for i in '\{\}[]'}).split(',')
                geom = [i[6:] for i in geom]

                # Create POLYGON geometry string
                geomString = ''
                geomClosePoint = geom[1] + ' ' + geom[0]
                geomString += geomClosePoint
                # First and last coordinate must match 
                for i in range(2, len(geom)-1,2):
                    point = ',' + str(geom[i+1]) + ' ' + str(geom[i])
                    geomString += point
                geomString += ',' + geomClosePoint
                queryGeom = '%s((%s))'%(shape, geomString)

                return queryGeom

            def getData(table):
                # Can instead SELECT x FROM x where contains is true for imporved performance
                cursor = connection.cursor()

                if table =='stop':
                    # Find all stops inside the polygon
                    # SELECT ST_CONTAINS(ST_GEOMFROMTEXT('SRID=4326;POLYGON((-9.232910089194776 55.677584411089526 ,-11.307128705084326 50.83647280350753,-4.5219720527529725 50.58044602533059,-4.9614251777529725 55.3591315224922,-9.232910089194776 55.677584411089526))'), shape_point.point), shape_point.point FROM shape_point ;
                    # SELECT ST_Contains(ST_GEOMFROMTEXT('SRID=4326;POLYGON((52.36620837113711 -9.263671925291419,52.204913551431154 -7.562988130375745,51.54291871811506 -7.993652326986195,51.646657472959326 -9.303222605958581,  52.36620837113711 -9.263671925291419))'), stop.point) , stop.point FROM stop ;
                    # SELECT ST_Contains(ST_GEOMFROMTEXT('SRID=4326;POLYGON((-9.263671925291419 52.36620837113711,-7.562988130375745 52.204913551431154,-7.993652326986195 51.54291871811506,-9.303222605958581 51.646657472959326,-9.263671925291419 52.36620837113711))'), stop.point)  , stop.point FROM stop ;
                    
                    query = "SELECT stop.name, (ST_AsText(stop.point)) FROM %s WHERE ST_Contains(ST_GeomFromText('SRID=4326;%s'), stop.point)"%(table, queryGeom)
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

                    query = "SELECT shape_id, (ST_AsText(shape.geometry)) FROM %s WHERE ST_Intersects(ST_GeomFromText('SRID=4326;%s'), shape.geometry)"%(table, queryGeom)
                    # query = "SELECT shape_id, (ST_AsGEOJSON(shape.geometry)) FROM %s WHERE ST_Intersects(ST_GeomFromText('SRID=4326;%s'), shape.geometry)"%(table, queryGeom)
                    cursor.execute(query)

                    shapes = cursor.fetchall()
                    # print(shapes)
                    return shapes

                elif table == 'trip':
                    # Find all trips inside polygon
                    query = "SELECT trip_id, (ST_AsText(trip.geometry)), shape_id FROM %s WHERE ST_Intersects(ST_GeomFromEWKT('SRID=4326;%s'), trip.geometry)"%(table, queryGeom)
                    cursor.execute(query)

                    trips = cursor.fetchall()
                    print(len(trips) )

                    return trips


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

        return render(request, 'default.html', {'form': form})

