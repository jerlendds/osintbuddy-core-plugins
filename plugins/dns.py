import json
import re
from osintbuddy.elements import TextInput, DropdownInput
from osintbuddy import transform, DiscoverableEntity, EntityRegistry


DNS_OPTIONS = [
    { "label": "NS" },
    { "label": "A" },
    { "label": "AAAA" },
    { "label": "CNAME" },
    { "label": "MX" },
    { "label": "SOA" },
    { "label": "TXT" },
    { "label": "PTR" },
    { "label": "SRV" },
    { "label": "CERT" },
    { "label": "DCHID" },
    { "label": "DNAME" }
]

class DNS(DiscoverableEntity):
    label = "DNS"
    icon = "directions"
    color = "#2181B5"

    properties = [
        TextInput(label="Value", icon="file-description"),
        DropdownInput(label="Record Type", options=DNS_OPTIONS)
    ]

    author = ["Team@ICG", "Bugfest"]
    description = "Represents DNS records with editable Value and Record Types, essential for mapping domain names to IP addresses"
    
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

    @transform(label="Extract IP", icon="microscope")
    async def transform_extract_ip(self, context, use) -> list:
        data = context.value
        ip_regexp = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        results = []
        ip_entity = await EntityRegistry.get_plugin('ip')
        for ip in ip_regexp.findall(data):
            transform_result = ip_entity.create(ip_address=ip)
            results.append(transform_result)
        return results


