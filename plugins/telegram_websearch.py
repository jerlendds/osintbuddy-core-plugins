import osintbuddy as ob
from osintbuddy.elements import TextInput

class TelegramWebsearch(ob.Plugin):
    label = 'Telegram Websearch'
    color = '#2AABEE'
    icon = 'brand-telegram'

    author = 'the OSINTBuddy team'
    description = 'Surface telegram communities from across the web'

    node = [
        TextInput(label='Query', icon='search', placeholder='Search Telegram...')
    ]

    telegram_cse_urls = [
        "https://cse.google.com/cse?&cx=006368593537057042503:efxu7xprihg",
        "https://cse.google.com/cse?cx=006368593537057042503:efxu7xprihg#gsc.tab=0",
        "https://cse.google.com/cse?cx=006368593537057042503:efxu7xprihg#gsc.tab=0&gsc.",
        "https://cse.google.com/cse?&cx=006368593537057042503:efxu7xprihg#gsc.tab=0",
        "https://cse.google.com/cse?cx=004805129374225513871:p8lhfo0g3hg",
        "https://cse.google.com/cse?cx=004805129374225513871%3Ap8lhfo0g3hg",
    ]

    @ob.transform(label='To CSE Search', icon='')
    async def transform_to_websearch(self, node, use):
        CSESearchPlugin = await ob.Registry.get_plugin('cse_search')
        cse_plugin = CSESearchPlugin()
        results = []
        for url in self.telegram_cse_urls:
            resp = await cse_plugin.get_cse_results(query=node.query, cse_url=url)
            results.append(await cse_plugin._map_cse_to_blueprint(resp=resp))
        return [result for cse_page in results for result in cse_page]
