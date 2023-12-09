import httpx
from selenium.webdriver.common.by import By
from osintbuddy.elements import TextInput, Text, Title, Empty, DropdownInput, CopyText
from osintbuddy.errors import OBPluginError, NodeMissingValueError
import httpx
import osintbuddy as ob



class GoogleCacheSearch(ob.Plugin):
    label = "Cache Search"
    color = "#145070"
    node = [
        TextInput(label="Query", icon="search"),
        TextInput(label="Pages", icon="123", default="3"),
    ]
    author = "the OSINTBuddy team"
    description = "Search the google cache"
    icon = "brand-google-filled"
    
    @ob.transform(label="To cache results")
    async def transform_to_google_cache_results(self, node, use):
        return await self.search_google_cache(node.query, node.pages)

    async def search_google_cache(self, query, pages):
        cache_results = []
        if not query:
            raise NodeMissingValueError("Query is a required field")
        try:
            async with httpx.AsyncClient() as client:
                google_resp = await client.get(
                    f'http://microservice:1323/google-cache?query={query}&pages={pages}',
                    timeout=None
                )
                cache_results = google_resp.json()
        except Exception:
            raise OBPluginError(
                "We ran into an error crawling googles cache. Please try again."
            )
        results = []
        GoogleCacheResult = await ob.Registry.get_plugin('cache_result')
        for result in self._parse_cache_results(
            cache_results
        ).get("results"):
            blueprint = GoogleCacheResult.blueprint(
                result={
                    "title": result.get("title"),
                    "text": result.get("description"),
                    "subtitle": result.get("breadcrumb"),
                },
                url=result.get("url"),
            )
            results.append(blueprint)
        return results

    def _parse_cache_results(self, cache_results):
        stats = cache_results.get("stats")
        related_searches = []
        result_stats = []
        if stats is not None:
            for stat in stats:
                if res := stat.get("result"):
                    result_stats = result_stats + res
                if related := stat.get("related"):
                    related_searches = related_searches + related

        results = []
        for key in cache_results.keys():
            if key is not None and key != "stats" and key != "questions":
                if cache_results.get(key):
                    for result in cache_results.get(key):
                        search_result = {
                            "index": result.get("index"),
                            "title": result.get("title"),
                            "description": result.get("description"),
                            "url": result.get("link"),
                            "breadcrumb": result.get("breadcrumb"),
                            "result_type": key,
                        }
                        results.append(search_result)
        return {
            "related": related_searches,
            "stats": result_stats,
            "results": results,
        }
