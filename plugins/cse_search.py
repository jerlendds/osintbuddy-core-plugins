import json
import urllib
from collections import defaultdict
from pydantic import BaseModel
import httpx
import requests
from osintbuddy.elements import TextInput, DropdownInput
from osintbuddy.errors import OBPluginError
import osintbuddy as ob


resp = requests.get('https://gist.githubusercontent.com/jerlendds/741d110f59a7d2ed2098325d30b00569/raw/25c15621eb67845db4ad65fc4ea8d3ad0991356f/cses.json')
cse_link_options = json.loads(resp.text)


class CSESearchPlugin(ob.Plugin):
    label = "CSE Search"

    description = 'Search through hundreds of categorized custom search engines provided by Google'
    author = 'the OSINTBuddy team'

    color = "#2C7237"
    node = [
        [
            TextInput(label="Query", icon="search"),
            TextInput(label="Pages", icon="123", default="1"),
        ],
        DropdownInput(label="CSE Categories", options=cse_link_options)
    ]

    async def get_cse_results(self, query, cse_url):
        try:
            async with httpx.AsyncClient() as client:
                # @todo add support for n pages... {node.pages}
                parsed_url = urllib.parse.urlparse(cse_url)
                cse_id = urllib.parse.parse_qs(parsed_url.query)["cx"][0]
                resp = await client.get(
                    f'http://microservice:1323/google-cse?query={query}&pages={"1"}&id={cse_id}',
                    timeout=None
                )
                return defaultdict(None, **resp.json())
        except Exception:
            raise OBPluginError(
                "There was an error fetching CSE results. Please try again later"
            )

    async def _map_cse_to_blueprint(self, resp):
        results = []
        CSESearchResult = await ob.Registry.get_plugin('cse_result')
        if resp and resp.get("results"):
            for result in resp["results"]:
                burl = result.get("breadcrumbUrl")
                blueprint = CSESearchResult.blueprint(
                    result={
                        "title": result.get("titleNoFormatting"),
                        "subtitle": burl.get("host") + str(burl.get("crumbs")),
                        "text": result.get("contentNoFormatting"),
                    },
                    url=result.get("unescapedUrl"),
                    cache_url=result.get("cacheUrl"),
                )
                results.append(blueprint)
        return results

    @ob.transform(label="To cse results", icon="search")
    async def transform_to_cse_results(self, node: BaseModel, **kwargs):
        url = node.cse_categories
        if not url:
            raise OBPluginError('The CSE Category field is required to transform.')
        resp = await self.get_cse_results(node.query, url)
        return await self._map_cse_to_blueprint(resp)
