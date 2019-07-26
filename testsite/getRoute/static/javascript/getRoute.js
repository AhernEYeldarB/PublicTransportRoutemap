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
    constructor() {
        this.baseMap = this.initMap();
    }

    initMap() {
        var baseMap = L.map('map').setView([51.8983, -8.4726], 12);

        // Limited to 75,000  free mapviews a mont ****
        var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
            // 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        });
        OpenStreetMap_Mapnik.addTo(baseMap);
        return baseMap
    }


    makeLine(coords, opacity='0.6', color='cyan') {
        // get coords from string input
        coords = coords.split('(');
        coords = coords[1].slice(0, -1);
        coords = coords.split(',');


        coords[0] = coords[0].split(/[ ]+/).map(Number).reverse();
        // Remove trailing whitespace
        for (let i = 1; i < coords.length; i++) {
            coords[i] = coords[i].substr(1).split(/[ ]+/).map(Number).reverse();
        };


        var line = L.polyline(coords, {
            color: color,
            width: 0.5,
            opacity: opacity,
            smoothFactor: 2,
        }).addTo(this.baseMap);

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
}