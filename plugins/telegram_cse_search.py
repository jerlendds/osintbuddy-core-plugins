from osintbuddy import transform, DiscoverableEntity, EntityRegistry
from osintbuddy.elements import TextInput

class TelegramCseSearch(DiscoverableEntity):
    label = "Telegram CSE Search"
    icon = "brand-telegram"
    color = "#2AABEE"

    properties = [
        TextInput(label="Query", icon="search")
    ]

    author = "Team@ICG"
    description = "A cloud-based, cross-platform instant messaging service"

    telegram_cse_urls = [
        "https://cse.google.com/cse?&cx=006368593537057042503:efxu7xprihg",
        "https://cse.google.com/cse?cx=004805129374225513871:p8lhfo0g3hg",
    ]

    @transform(label='To CSE Search', icon='')
    async def transform_to_websearch(self, node, use):
        cse_search_entity = await EntityRegistry.get_plugin('google_cse_search')
        cse_plugin = cse_search_entity()
        results = []
        for url in self.telegram_cse_urls:
            resp = await cse_plugin.get_cse_results(query=node.query, cse_url=url)
            results.append(await cse_plugin._map_cse_to_blueprint(resp=resp))
        return [result for cse_page in results for result in cse_page]
