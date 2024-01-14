from osintbuddy.elements import Title, Empty, TextInput
from osintbuddy import transform, DiscoverableEntity, EntityRegistry

class IPGeolocation(DiscoverableEntity):
    label = "IP Geolocation"
    icon = "map-pin"
    color = "#FFCC33"
    show_label = False

    properties = [
        [
            TextInput(label="City", icon="map-pin"),
            TextInput(label="ASN", icon="access-point"),
        ],
        [
            TextInput(label="State", icon="map-pin"),
            TextInput(label="Hostname", icon="access-point"),
        ],
        [
            TextInput(label="Country", icon="map-pin"),
            TextInput(label="Range", icon="access-point"),
        ],
        [
            TextInput(label="Postal", icon="map-pin"),
            TextInput(label="Company", icon="trademark"),
        ],
        [
            TextInput(label="Timezone", icon="clock"),
            TextInput(label="Hosted domains", icon="access-point"),
        ],
        [
            TextInput(label="Coordinates", icon="map-pin"),
            TextInput(label="Privacy", icon="network"),
        ],
        [
            Empty(),
            TextInput(label="Anycast", icon="network"),
        ],
        [
            Empty(),
            TextInput(label="ASN type", icon="access-point"),
        ],
        [
            Empty(),
            TextInput(label="Abuse Contact", icon="map-pin"),
        ],
    ]

    author = "Team@ICG"
    description = "The geolocation estimate for a device connected to a computer network "

