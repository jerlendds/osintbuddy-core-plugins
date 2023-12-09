import json
import re
import socket

import httpx
from urllib.parse import urlparse
import dns.resolver
from selenium.webdriver.common.by import By
from osintbuddy.elements import TextInput, Text, Title, Empty, DropdownInput, CopyText
from osintbuddy.errors import OBPluginError, NodeMissingValueError
from osintbuddy.utils import to_camel_case
import urllib
from collections import defaultdict
import httpx
import osintbuddy as ob
from pydantic import BaseModel



class GoogleSearch(ob.Plugin):
    label = "Google Search"
    color = "#3D78D9"
    node = [
        TextInput(label="Query", icon="search"),
        TextInput(label="Pages", icon="123", value="3"),
    ]
    icon = "brand-google-filled"
    author = "the OSINTBuddy team"
    description = "Search google using the advanced operators you're used to"

    @ob.transform(label="To results")
    async def transform_to_google_results(self, node, use):
        # print("@todo refactor transform node API: ", node)
        results = []
        google_result_entity = await ob.Registry.get_plugin('google_result')
        for result in await self.search_google(node.query, node.pages):
            blueprint = google_result_entity.blueprint(
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
