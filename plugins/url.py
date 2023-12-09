from urllib.parse import urlparse
from osintbuddy.elements import TextInput
import osintbuddy as ob


class URL(ob.Plugin):
    label = "URL"
    color = '#642CA9'
    node = [
        TextInput(label="URL", icon="link"),
    ]
    author = "the OSINTBuddy team"
    icon = "link"

    @ob.transform(label="To website", icon="world-www")
    async def transform_to_website(self, node, **kwargs):
        WebsitePlugin = await ob.Registry.get_plugin('website')
        domain = urlparse(node.url).netloc
        return WebsitePlugin.blueprint(domain=domain)
