from osintbuddy.elements import Title, CopyText, Text
from osintbuddy import transform, DiscoverableEntity, EntityRegistry

class GoogleCSEResult(DiscoverableEntity):
    label = "Google CSE Result"
    icon = "brand-google-filled"
    color = "#058F63"
    show_label = False
    
    properties = [
        Title(label="title"),
        Text(label="breadcrumb"),
        Text(label="content"),
        CopyText(label="URL"),
        CopyText(label="Cache URL"),
    ]

    author = "Team@ICG"
    description = "Custom Search Engine Results from Google"

    @transform(label="To URL", icon='link')
    async def transform_to_url(self, node, **kwargs):
        url_entity = await EntityRegistry.get_plugin('url')
        return url_entity.create(url=node.url)
