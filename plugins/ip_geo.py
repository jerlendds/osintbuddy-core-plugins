from osintbuddy.elements import Text, Title, Empty
import osintbuddy as ob

class IPGeoPlugin(ob.Plugin):
    label = "IP Geo"
    show_label = False

    author = 'the OSINTBuddy team'

    color = "#FFCC33"
    node = [
        [
            Title(label="geolocation-data", title="IP Geolocation"),
            Title(label="summary-data", title="Summary"),
        ],
        [
            Text(label="City", icon="map-pin"),
            Text(label="ASN", icon="access-point"),
        ],
        [
            Text(label="State", icon="map-pin"),
            Text(label="Hostname", icon="access-point"),
        ],
        [
            Text(label="Country", icon="map-pin"),
            Text(label="Range", icon="access-point"),
        ],
        [
            Text(label="Postal", icon="map-pin"),
            Text(label="Company", icon="trademark"),
        ],
        [
            Text(label="Timezone", icon="clock"),
            Text(label="Hosted domains", icon="access-point"),
        ],
        [
            Text(label="Coordinates", icon="map-pin"),
            Text(label="Privacy", icon="network"),
        ],
        [
            Empty(),
            Text(label="Anycast", icon="network"),
        ],
        [
            Empty(),
            Text(label="ASN type", icon="access-point"),
        ],
        [
            Empty(),
            Text(label="Abuse Contact", icon="map-pin"),
        ],
    ]

