from urllib.parse import urlparse
from osintbuddy.elements import TextInput
from osintbuddy import transform, DiscoverableEntity, EntityRegistry



class URL(DiscoverableEntity):
    label = "URL"
    icon = "link"
    color = '#642CA9'

    properties = [
        TextInput(label="URL", icon="link"),
    ]

    author = "Team@ICG"
    description = ""

    @transform(label="To website", icon="world-www")
    async def transform_to_website(self, node, **kwargs):
        website_entity = await EntityRegistry.get_plugin('website')
        domain = urlparse(node.url).netloc
        return website_entity.create(domain=domain)
