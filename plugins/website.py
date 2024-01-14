import socket
from urllib.parse import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from osintbuddy.elements import TextInput
from osintbuddy.errors import OBPluginError, NodeMissingValueError
from osintbuddy import transform, DiscoverableEntity, EntityRegistry


class Website(DiscoverableEntity):
    label = "Website"
    icon = "world-www"
    color = "#005AA6"

    properties = [
        TextInput(label="Domain", icon="world-www"),
    ]

    author = "Team@ICG"
    description = "Web pages and related content that is identified by a domain name"

    @transform(label="To IP", icon="building-broadcast-tower")
    async def to_ip(self, node, use):
        ip_entity = await EntityRegistry.get_plugin('ip')
        transform = ip_entity.create(
            ip_address=socket.gethostbyname(node.domain)
        )
        return transform

    @transform(label="To google", icon="world")
    async def to_google(self, node, use):
        results = []
        google_search_entity = await EntityRegistry.get_plugin('google_search')
        for result in await google_search_entity().search_google(
            query=node.domain, pages="3"
        ):
            google_result_entity = await EntityRegistry.get_plugin('google_result')
            blueprint = google_result_entity.create(
                result={
                    "title": result.get("title"),
                    "subtitle": result.get("breadcrumb"),
                    "text": result.get("description"),
                },
                url=result.get("url"),
            )
            results.append(blueprint)
        return results

    @transform(label="To WHOIS", icon="world")
    async def to_whois(self, node, use):
        domain = node.domain
        if len(domain.split(".")) > 2:
            domain = domain.split(".")
            domain = domain[len(domain) - 2] + "." + domain[len(domain) - 1]

        with use.get_driver() as driver:
            driver.get(f"https://www.whois.com/whois/{domain}")
            raw_whois = ""
            try:
                WebDriverWait(driver, 90).until(
                    EC.text_to_be_present_in_element(By.TAG_NAME, "pre")
                )
                raw_whois = driver.find_element(
                    by=By.TAG_NAME, value="pre"
                ).text
            except Exception as e:
                print(e)
                raise OBPluginError(
                    "Captcha encountered, please try again later."
                )
            whois_entity = await EntityRegistry.get_plugin("whois")
            
            return whois_entity.create(
                whois_data="\n".join(self._parse_whois(raw_whois)),
                raw_whois_data=raw_whois
            )

    @transform(label="To DNS", icon="world")
    async def to_dns(self, node, use):
        dns_entity = await EntityRegistry.get_plugin('dns')
        data = dns_entity.data_template()

        if len(node.domain) == 0:
            raise NodeMissingValueError(
                "A website is required to process dns records"
            )

        website = node.domain
        website_parsed = urlparse(website)
        if website_parsed.scheme:
            domain = website_parsed.netloc
        else:
            domain = urlparse(f"https://{website}").netloc

        for key in data.keys():
            try:
                resolved = dns.resolver.resolve(domain, key)
                data[key] = [str(answer) for answer in resolved]
            except Exception:
                pass
        results = []
        data_filled = dict((k, v) for k, v in data.items() if v is not None)
        for key, value in data_filled.items():
            for entry in value:
                record_type = dns_entity.record(key, entry)
                record = record_type["text"]
                del record_type["text"]
                blueprint = dns_entity.create(
                    record_type=record_type,
                    value=record,
                )
                results.append(blueprint)
        return results

    @staticmethod
    def _parse_whois(whois_data):
        data = []
        for line in whois_data.split("\n"):
            if "DNSSEC" in line:
                data.append(line)
                break
            else:
                data.append(line)
        return data