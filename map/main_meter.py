import folium
import json
from geopy.distance import geodesic
import os

# -------------------------------
# 讀取初始軌跡
with open("data/sample_track.json", "r", encoding="utf-8") as f:
    track_points = json.load(f)

# -------------------------------
# 建立地圖
m = folium.Map(location=track_points[0], zoom_start=17)

# -------------------------------
# 繪製初始軌跡
prev_point = None
for i, point in enumerate(track_points):
    folium.CircleMarker(
        location=point,
        radius=5,
        color="blue",
        fill=True,
        fill_color="blue",
        popup=f"點 {i+1}"
    ).add_to(m)
    
    if prev_point:
        dist = geodesic(prev_point, point).meters
        mid_lat = (prev_point[0] + point[0]) / 2
        mid_lon = (prev_point[1] + point[1]) / 2
        folium.Marker(
            location=(mid_lat, mid_lon),
            icon=folium.DivIcon(
                html=f'<div style="font-size:12px;color:red;">{dist:.2f} m</div>'
            )
        ).add_to(m)
        folium.PolyLine(
            locations=[prev_point, point],
            color="green" if dist < 50 else "orange",
            weight=3
        ).add_to(m)
    
    prev_point = point

# -------------------------------
# 互動功能：新增點、刪除最後一個、切換單位、累積距離
click_js = """
var unit = 'm';  // 'm' 或 'cm'
var totalDistance = 0;
var markers = [];
var lines = [];

function toRad(x) { return x * Math.PI / 180; }

function calcDistance(p1, p2) {
    var R = 6371000; // 地球半徑
    var lat1 = p1.lat;
    var lon1 = p1.lng;
    var lat2 = p2.lat;
    var lon2 = p2.lng;
    var dLat = toRad(lat2-lat1);
    var dLon = toRad(lon2-lon1);
    var a = Math.sin(dLat/2)*Math.sin(dLat/2) +
            Math.cos(toRad(lat1))*Math.cos(toRad(lat2))*
            Math.sin(dLon/2)*Math.sin(dLon/2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c;
    return d;
}

function updateDistanceLabel(d) {
    var value = unit === 'm' ? (d/1).toFixed(2) + ' m' : (d*100).toFixed(1) + ' cm';
    return value;
}

function addMarker(e) {
    var newLatLng = e.latlng;
    var marker = L.marker(newLatLng).addTo(map);
    markers.push(marker);

    if (markers.length > 1) {
        var last = markers[markers.length-2];
        var dist = calcDistance(last.getLatLng(), newLatLng);
        totalDistance += dist;
        var midLat = (last.getLatLng().lat + newLatLng.lat)/2;
        var midLng = (last.getLatLng().lng + newLatLng.lng)/2;

        var line = L.polyline([last.getLatLng(), newLatLng],
                              {color: dist < 50 ? 'green' : 'orange', weight: 3}).addTo(map);
        lines.push(line);

        L.marker([midLat, midLng], {
            icon: L.divIcon({className:'distance-label', html:'<div style="color:red;font-size:12px;">'+updateDistanceLabel(dist)+'</div>'})
        }).addTo(map);
    }

    updateTotalDistance();
}

function deleteLastMarker() {
    if (markers.length === 0) return;
    var last = markers.pop();
    map.removeLayer(last);
    if (lines.length > 0) {
        var line = lines.pop();
        map.removeLayer(line);
    }
    // 重新計算 totalDistance
    totalDistance = 0;
    for (var i=1; i<markers.length; i++) {
        totalDistance += calcDistance(markers[i-1].getLatLng(), markers[i].getLatLng());
    }
    updateTotalDistance();
}

function toggleUnit() {
    unit = unit === 'm' ? 'cm' : 'm';
    updateTotalDistance();
}

function updateTotalDistance() {
    var label = document.getElementById('totalDistance');
    if (!label) {
        label = L.control({position: 'topright'});
        label.onAdd = function(map) {
            var div = L.DomUtil.create('div', 'distance-total');
            div.id = 'totalDistance';
            div.style.backgroundColor = 'white';
            div.style.padding = '5px';
            div.style.fontSize = '14px';
            div.style.fontWeight = 'bold';
            div.style.border = '1px solid gray';
            return div;
        }
        label.addTo(map);
    }
    document.getElementById('totalDistance').innerHTML = '累積距離: ' + updateDistanceLabel(totalDistance);
}

// ----------------- 按鈕
var btnDiv = L.control({position: 'topleft'});
btnDiv.onAdd = function(map) {
    var div = L.DomUtil.create('div', 'btn-div');
    div.innerHTML = '<button onclick="deleteLastMarker()" style="margin:2px;">刪除最後一點</button>' +
                    '<button onclick="toggleUnit()" style="margin:2px;">切換單位</button>';
    return div;
}
btnDiv.addTo(map);

map.on('click', addMarker);
updateTotalDistance();
"""

m.get_root().html.add_child(folium.Element(f'<script>{click_js}</script>'))

# -------------------------------
# 輸出互動地圖
output_path = "output/interactive_map.html"
os.makedirs("output", exist_ok=True)
m.save(output_path)
print(f"互動地圖已生成：{output_path}")
