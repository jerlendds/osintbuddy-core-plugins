import json, re, random
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
import httpx

from osintbuddy.elements import TextInput, DropdownInput
from osintbuddy.errors import OBPluginError
from osintbuddy import transform, DiscoverableEntity, EntityRegistry

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

cse_link_options = []
try:
    import requests
    resp = requests.get('https://gist.githubusercontent.com/jerlendds/741d110f59a7d2ed2098325d30b00569/raw/25c15621eb67845db4ad65fc4ea8d3ad0991356f/cses.json')
    cse_link_options = json.loads(resp.text)
except Exception as e:
    print('Error loading CSE categories!', e)


class CSESearch(DiscoverableEntity):
    label = "CSE Search"
    icon = "brand-google-filled"
    color = "#2C7237"

    properties = [
        [
            TextInput(label="Query", icon="search"),
            DropdownInput(label="Max Results", value={"label": "100"}, options=[
                { "label": "10" },
                { "label": "20" },
                { "label": "30" },
                { "label": "40" },
                { "label": "50" },
                { "label": "60" },
                { "label": "70" },
                { "label": "80" },
                { "label": "90" },
                { "label": "100" }
            ]),
        ],
        DropdownInput(label="CSE Categories", options=cse_link_options)
    ]

    author = "Team@ICG"
    description = 'Search through hundreds of categorized custom search engines from Google'

    async def _map_cse_to_blueprint(self, resp):
        entities = []
        cse_search_result = await EntityRegistry.get_plugin('cse_result')
        if results := resp.get("results"):
            for result in results:
                breadcrumb = result.get("breadcrumbUrl", {})
                blueprint = cse_search_result.create(
                    title=result.get("titleNoFormatting"),
                    content=result.get("contentNoFormatting"),
                    breadcrumb=f"{breadcrumb.get('host')} {' '.join(breadcrumb.get('crumbs', []))}",
                    url=result.get("unescapedUrl"),
                    cache_url=result.get("cacheUrl"),
                )
                entities.append(blueprint)
        return entities

    @transform(label="To cse results", icon="search")
    async def transform_to_cse_results(self, node, use):
        if not node.cse_categories:
            raise OBPluginError('The CSE Category field is required to transform.')
        cse_results = await self.get_cse_results(node.query, node.cse_categories, node.max_results)
        return await self._map_cse_to_blueprint(cse_results)

    async def get_cse_results(self, query, url, max_results=100):
        parsed_url = urlparse(url)
        url_params = parse_qs(parsed_url.query)
        cx_param = url_params["cx"][0]

        re_token = re.compile(r'(?<=cse_token":\s")(.*?)(?=")')
        re_exp = re.compile('(?<=exp":\s)(.*?)(])')
        re_cse_lib_version = re.compile('(?<=cselibVersion":\s")(.*?)(?=")')
        async with httpx.AsyncClient() as client:
            results_response = await client.get(f"https://cse.google.com/cse.js?sca_esv={cx_param.split(':')[0][0:11]}&hpg=1&cx={cx_param}", headers=headers)
            html = results_response.content.decode("utf8")
            cse_token = re_token.search(html)[1]
            exp = re_exp.search(html)[1]
            cse_lib_version = re_cse_lib_version.search(html)[1]
            cb_value = f"{random.randint(1, 10000)}"
            callback = "google.search.cse.api" + cb_value
        
        
            g_api_params = {
                "rsz": "filtered_cse",
                "num": max_results
            }
        
            g_api_params["hl"] = "en"
            g_api_params["source"] = "gcsc"
            g_api_params["gss"] = ".com"
            g_api_params["cselibv"] = cse_lib_version
            g_api_params["cx"] = cx_param
            g_api_params["q"] = query
            g_api_params["safe"] = "off"
            g_api_params["cse_tok"] = cse_token
            g_api_params["sort"] = ""
            g_api_params["exp"] = exp
            g_api_params["oq"] = query
            g_api_params["cseclient"] = "hosted-page-client"
            g_api_params["callback"] = callback
        
            cse_results_url = "https://cse.google.com/cse/element/v1?" + urlencode(g_api_params)
            results_response = await client.get(cse_results_url, headers=headers)
            results_data = results_response.content.decode("utf8")
            cse_json_str = results_data[30 + len(cb_value):-2].encode("utf8")
            cse_search_results = json.loads(cse_json_str)
            return cse_search_results
