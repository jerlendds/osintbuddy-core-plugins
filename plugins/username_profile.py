from osintbuddy.elements import TextInput
import osintbuddy as ob

class UsernameProfile(ob.Plugin):
    label = "Username Profile"
    show_label = False
    color = "#D842A6"
    icon = "user-scan"
    author = "the OSINTBuddy team"
    
    entity = [
        TextInput(label='Link', icon='link'),
        TextInput(label='Category', icon='category'),
        TextInput(label='Site', icon='world'),
        TextInput(label='Username', icon='user'),
    ]

    @ob.transform(label="To URL", icon="link")
    async def transform_to_url(self, node, use):
        url_entity = await ob.Registry.get_plugin('url')
        url_node = url_entity.blueprint(
            url=node.link
        )
        return url_node
