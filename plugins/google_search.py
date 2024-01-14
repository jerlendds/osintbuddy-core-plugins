import httpx
from osintbuddy.elements import TextInput
from osintbuddy.errors import OBPluginError, NodeMissingValueError
from osintbuddy import transform, DiscoverableEntity, EntityRegistry




class GoogleSearch(DiscoverableEntity):
    label = "Google Search"
    icon = "brand-google-filled"
    color = "#3D78D9"

    properties: list[TextInput] = [
        TextInput(label="Query", icon="search"),
        TextInput(label="Pages", icon="123", value="3"),
    ]

    author = "Team@ICG"
    description = "Search google using the advanced operators you're used to"

    @transform(label="To results")
    async def transform_to_google_results(self, node, use):
        # print("@todo refactor transform node API: ", node)
        results = []
        google_result_entity = await EntityRegistry.get_plugin('google_result')
        for result in await self.search_google(node.query, node.pages):
            blueprint = google_result_entity.create(
                result={
                    "title": result.get("title"),
                    "subtitle": result.get("breadcrumb"),
                    "text": result.get("description"),
                },
                url=result.get("url"),
            )
            results.append(blueprint)
        return results

    def _parse_google_data(self, results) -> dict:
        stats = results.get("stats")
        related_searches = []
        result_stats = []
        if stats is not None:
            for stat in stats:
                if res := stat.get("result"):
                    result_stats = result_stats + res
                if related := stat.get("related"):
                    related_searches = related_searches + related
        output = []
        for key in list(results.keys()):
            if key is not None and key != "stats" and key != "questions":
                if results.get(key):
                    for result in results.get(key):
                        search_result = {
                            "index": result.get("index"),
                            "title": result.get("title"),
                            "description": result.get("description"),
                            "url": result.get("link"),
                            "breadcrumb": result.get("breadcrumb"),
                            "question": result.get("question"),
                            "result_type": key,
                        }
                        output.append(search_result)
        return {
            "stats": result_stats,
            "related": related_searches,
            "results": output,
        }

    async def search_google(self, query, pages):
        if not query:
            raise NodeMissingValueError("Query is a required field")
        try:
            async with httpx.AsyncClient() as client:
                google_resp = await client.get(
                    f'http://microservice:1323/google?query={query}&pages={pages}',
                    timeout=None
                )
                google_results = google_resp.json()
        except OBPluginError:
            raise OBPluginError((
                "There was an error crawling Google. Please try again."
                "If you keep encountering this error please open an issue on Github."
            ))

        results = self._parse_google_data(google_results)["results"]
        return results
