import json
import re
from osintbuddy.elements import Title, TextInput
import osintbuddy as ob



class DNS(ob.Plugin):
    label = "DNS"
    color = "#2181B5"
    icon = "server-2"
    node = [
        Title(label="record_type"),
        TextInput(label="Value", icon="map-pin")
    ]

    _items = [
        "NS",
        "A",
        "AAAA",
        "CNAME",
        "MX",
        "SOA",
        "TXT",
        "PTR",
        "SRV",
        "CERT",
        "DCHID",
        "DNAME",
    ]

    author = ['the OSINTBuddy team', 'Bugfest']

    @classmethod
    def data_template(cls):
        return {k: None for k in cls._items}

    @staticmethod
    def record(key, data):
        _data = json.dumps(data).strip("'\" .")
        match key:
            case "MX":
                matches = re.findall(r"\d+ (.*)", _data)
                _data = matches[0] if len(matches) else _data
            case "TXT":
                _data = _data.strip('\\"')

        return {
            "title": None,
            "subtitle":  f"{key} Record",
            "text": _data,
        }

    @ob.transform(label="Extract IP", icon="microscope")
    async def transform_extract_ip(self, node, use) -> list:
        data = node.value
        ip_regexp = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        results = []
        IPAddressPlugin = await ob.Registry.get_plugin('ip')
        for ip in ip_regexp.findall(data):
            blueprint = IPAddressPlugin.blueprint(ip_address=ip)
            results.append(blueprint)
        return results


