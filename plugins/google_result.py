import osintbuddy as ob
from osintbuddy.elements import Title, CopyText
from urllib.parse import urlparse


class GoogleResult(ob.Plugin):
    label = "Google Result"
    show_label = False
    color = "#308e49"
    node = [Title(label="result"), CopyText(label="url")]

    @ob.transform(label="To website", icon="world")
    async def transform_to_website(self, node, use):
        WebsitePlugin = await ob.Registry.get_plugin('website')
        blueprint = WebsitePlugin.blueprint(
            domain=urlparse(node.url).netloc
        )
        return blueprint
