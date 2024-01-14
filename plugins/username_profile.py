from osintbuddy.elements import TextInput
from osintbuddy import transform, DiscoverableEntity, EntityRegistry

class UsernameProfile(DiscoverableEntity):
    label = "Username Profile"
    icon = "user-scan"
    color = "#D842A6"
    show_label = False

    properties = [
        TextInput(label='Link', icon='link'),
        TextInput(label='Category', icon='category'),
        TextInput(label='Site', icon='world'),
        TextInput(label='Username', icon='user'),
    ]
    
    author = "Team@ICG"
    description = "Digital social profiles for multiple platforms with categories"

    @transform(label="To URL", icon="link")
    async def transform_to_url(self, node, use):
        url_entity = await EntityRegistry.get_plugin('url')
        url_node = url_entity.create(
            url=node.link
        )
        return url_node
