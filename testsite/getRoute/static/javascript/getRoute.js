// explore = {
//     mapPoint: function(map_id, x, y, zoom) {
//         var map = new OpenLayers.Map(map_id);
//         var osm = new OpenLayers.Layer.OSM("OpenStreetMap Map");
//         var fromProjection = new OpenLayers.Projection("EPSG:4326");
//         var toProjection = new OpenLayers.Projection("EPSG:900913");
//         var position = new OpenLayers.LonLat(x, y).transform(fromProjection, toProjection);
//         map.addLayer(osm);

//         var markers = new OpenLayers.Layer.Markers( "Markers" );
//         map.addLayer(markers);
//         markers.addMarker(new OpenLayers.Marker(position));

//         map.setCenter(position, zoom);
//     },
//     mapLine: function(map_id, line_wkt) {
//         var map = new OpenLayers.Map(map_id);
//         var osm = new OpenLayers.Layer.OSM("OpenStreetMap Map");
//         var fromProjection = new OpenLayers.Projection("EPSG:4326");
//         var toProjection = new OpenLayers.Projection("EPSG:900913");
//         map.addLayer(osm);

//         var style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
//         style.strokeColor = "red";
//         style.strokeColor = "red";
//         style.fillColor = "red";
//         style.pointRadius = 10;
//         style.strokeWidth = 3;
//         style.rotation = 45;
//         style.strokeLinecap = "butt";
//         var vectorLayer = new OpenLayers.Layer.Vector("Line", {'style': style});
//         var wkt = new OpenLayers.Format.WKT({
//             'internalProjection': toProjection,
//             'externalProjection': fromProjection,
//             'style': style });
//         var lineVector = wkt.read(line_wkt);
//         var bounds = lineVector.geometry.getBounds();

//         map.addLayer(vectorLayer);
//         vectorLayer.addFeatures([lineVector]);

//         map.zoomToExtent(bounds);
//     }
// }
class DrawRoute {
    constructor(base) {
        if (typeof base != "undefined") {
            this.baseMap = base
        }
        else {
            this.baseMap = this.initMap();
        }
    }

    initMap() {
        var baseMap = L.map('map').setView([51.8983, -8.4726], 12);

        // Limited to 75,000  free mapviews a mont ****
        var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
            // 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        });
        // var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        //     maxZoom: 19,
        //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        // });
        OpenStreetMap_Mapnik.addTo(baseMap);
        return baseMap
    }

    fixCoordsWKT(coords) {
        // get coords from LINESTRING ewkd input 
        // Sometimes puts trailing space between coords sometimes doesnt???
        var x = 1
        
        coords = coords.split('(');
        coords = coords[1].slice(0, -1);
        coords = coords.split(',');
        

        coords[0] = coords[0].split(/[ ]+/).map(Number).reverse();
        if (coords.length > 1 && coords[1][0] === '-') {
            x = 0
        }
        // Remove trailing whitespace
        for (let i = 1; i < coords.length; i++) {
            coords[i] = coords[i].substr(x).split(/[ ]+/).map(Number).reverse();
        };
        return coords
    }

    fixCoordsGEOJSON(coords){
        // xreates coordinate string from GeoJSON format
        coords = JSON.parse(coords[1]).coordinates;
        for(let i=0; i< coords.length; i++){
            coords[i] = coords[i].reverse();
        };
        return coords
    }

    makeLine(coords, fix='wkt', opacity = '0.7', color = 'purple') {
        if (fix === 'wkt') {
            coords = this.fixCoordsWKT(coords);
        }
        else if(fix ==='geojson'){
            coords = this.fixCoordsGEOJSON(coords);
        }

        var line = L.polyline(coords, {
            color: color,
            width: 0.5,
            opacity: opacity,
            smoothFactor: 2,
        });

        line.on('mouseover', function (e) {
            var layer = e.target;
            layer.setStyle({
                color: 'purple',
                opacity: 1,
                weight: 5,
            });
            layer.bringToFront();
        });

        line.on('mouseout', function (e) {
            var layer = e.target
            layer.setStyle(
                {
                    color: color,
                    width: 0.5,
                    opacity: opacity,
                    smoothFactor: 2,
                    weight: 3,
                });
            layer.bringToBack();
        });
        return line
    }


    makePoint(coordLat, coordLon) {
        coordLat = Number(coordLat);
        coordLon = Number(coordLon);

        // console.log(coordLat, coordLon);
        var pointCirc = L.circleMarker([coordLat, coordLon], { radius: 10, color: 'white' }).addTo(this.baseMap);
        // var pointMarker = L.marker([coordLat, coordLon]).addTo(this.baseMap);
        return pointCirc
    }

    getColour() {
        function colour() {
            return String(parseInt(Math.random() * (+255 - 0) + 0))
        };
        function getColor() {
            return "rgb(" + colour() + "," + colour() + "," + colour() + ")"
        }
        return getColor()
    }
}