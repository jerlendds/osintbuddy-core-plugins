from osintbuddy import transform, DiscoverableEntity, EntityRegistry
from osintbuddy.elements import Title, CopyText
from urllib.parse import urlparse


class GoogleResult(DiscoverableEntity):
    label = "Google Result"
    icon = "brand-google-filled"
    color = "#308e49"
    show_label = False

    properties = [
        Title(label="result"),
        CopyText(label="url")
    ]

    author = "Team@ICG"
    description = "Search Engine Results powered by Google"

    @transform(label="To website", icon="world")
    async def transform_to_website(self, context, use):
        website_entity = await EntityRegistry.get_plugin('website')
        blueprint = website_entity.create(
            domain=urlparse(context.url).netloc
        )
        return blueprint
