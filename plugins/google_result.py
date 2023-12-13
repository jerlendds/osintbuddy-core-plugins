import osintbuddy as ob
from osintbuddy.elements import Title, CopyText
from urllib.parse import urlparse


class GoogleResult(ob.Plugin):
    label = "Google Result"
    show_label = False
    color = "#308e49"
    entity = [Title(label="result"), CopyText(label="url")]
    icon = "brand-google-filled"
    author = "the OSINTBuddy team"

    @ob.transform(label="To website", icon="world")
    async def transform_to_website(self, node, use):
        website_entity = await ob.Registry.get_plugin('website')
        blueprint = website_entity.blueprint(
            domain=urlparse(node.url).netloc
        )
        return blueprint
