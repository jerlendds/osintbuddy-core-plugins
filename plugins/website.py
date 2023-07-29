import socket
from urllib.parse import urlparse
import dns.resolver
from selenium.webdriver.common.by import By
from osintbuddy.elements import TextInput
from osintbuddy.errors import OBPluginError, NodeMissingValueError
import osintbuddy as ob


class Website(ob.Plugin):
    label = "Website"
    color = "#1D1DB8"
    icon = "world-www"
    node = [
        TextInput(label="Domain", icon="world-www"),
    ]

    author = 'the OSINTBuddy team'
    description = 'Reveal insights for any website'

    @ob.transform(label="To IP", icon="building-broadcast-tower")
    async def transform_to_ip(self, node, use):
        IPAddressPlugin = await ob.Registry.get_plugin('ip')
        blueprint = IPAddressPlugin.blueprint(
            ip_address=socket.gethostbyname(node.domain)
        )
        return blueprint

    @ob.transform(label="To google", icon="world")
    async def transform_to_google(self, node, use):
        # @todo
        results = []
        GoogleSearchPlugin = await ob.Registry.get_plugin('google_search')
        for result in await GoogleSearchPlugin().search_google(
            query=node.domain, pages="3"
        ):
            GoogleResult = await ob.Registry.get_plugin('google_result')
            blueprint = GoogleResult.blueprint(
                result={
                    "title": result.get("title"),
                    "subtitle": result.get("breadcrumb"),
                    "text": result.get("description"),
                },
                url=result.get("url"),
            )
            results.append(blueprint)
        return results

    @ob.transform(label="To WHOIS", icon="world")
    async def transform_to_whois(self, node, use):
        domain = node.domain
        if len(domain.split(".")) > 2:
            domain = domain.split(".")
            domain = domain[len(domain) - 2] + "." + domain[len(domain) - 1]

        with use.get_driver() as driver:
            driver.get(f"https://www.whois.com/whois/{domain}")
            raw_whois = None
            try:
                raw_whois = driver.find_element(
                    by=By.TAG_NAME, value="pre"
                ).text
            except Exception as e:
                print(e)
                raise OBPluginError(
                    "Captcha encountered, please try again later."
                )
            WhoisPlugin = await ob.Registry.get_plugin('whois')
            return WhoisPlugin.blueprint(
                raw_whois="\n".join(self._parse_whois(raw_whois))
            )

    @ob.transform(label="To DNS", icon="world")
    async def transform_to_dns(self, node, use):
        DnsPlugin = await ob.Registry.get_plugin('dns')
        data = DnsPlugin.data_template()

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
                blueprint = DnsPlugin.blueprint(
                    record=DnsPlugin.record(key, entry)
                )
                results.append(blueprint)
        return results

    # @ob.transform(label='To subdomains', icon='world')
    # async def transform_to_subdomains(self, node, use):
    #     # @todo
    #     return WebsitePlugin.blueprint(
    #         domain=urlparse(node['data'][3]).netloc
    #     )

    # @ob.transform(label='To emails', icon='world')
    # async def transform_to_emails(self, node, use):
    #     # @todo
    #     blueprint = WebsitePlugin.blueprint()
    #     website = node['data'][3]
    #     blueprint['elements'][0]['value'] = urlparse(website).netloc
    #     return blueprint
    # @ob.transform(label='To urlscan.io', icon='world')
    # async def transform_to_urlscanio(self, node, use):
    #     # @todo
    #     blueprint = WebsitePlugin.blueprint()
    #     domain = node['data'][0]
    #     if domain:
    #         domain = domain.replace('https://', '')
    #         domain = domain.replace('http://', '')
    #         params = {
    #             'q': quote(domain),
    #         }
    #         res = requests.get('https://urlscan.io/api/v1/search/', params=params)
    #     return blueprint

    @staticmethod
    def _parse_whois(whois_data):
        data = []
        for line in whois_data.split("\n"):
            if "DNSSEC" in line:
                data.append(line)
