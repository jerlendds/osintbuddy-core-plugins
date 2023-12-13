from osintbuddy.elements import Title, CopyText
import osintbuddy as ob

class CSESearchResultsPlugin(ob.Plugin):
    label = "CSE Result"
    show_label = False
    color = "#058F63"
    icon = "brand-google-filled"
    author = "the OSINTBuddy team"
    
    entity = [
        Title(label="result"),
        CopyText(label="URL"),
        CopyText(label="Cache URL"),
    ]

    @ob.transform(label="To URL", icon='link')
    async def transform_to_url(self, node, **kwargs):
        url_entity = await ob.Registry.get_plugin('url')
        return url_entity.blueprint(url=node.url)
