import urllib.parse

import pkg_resources
from aiohttp.web import Application, Response, Request, json_response
from tinydb import TinyDB, Query


async def error_page(request: Request) -> Response:
    return Response(text="Error loading analysis.")


class TrainingAssistantApplication(Application):

    def __init__(self, db_path: str):
        Application.__init__(self)

        add_analysis_resource = self.router.add_resource("/add/{hash}")
        add_analysis_resource.add_route('PUT', self.add_analysis)

        show_analysis_data_resource = self.router.add_resource("/data/{hash}")
        show_analysis_data_resource.add_route('GET', self.show_analysis_data)

        self.router.add_get("/error", error_page)

        self.router.add_static('/', pkg_resources.resource_filename(__name__, "public"))

        self.db = TinyDB(db_path)

    async def add_analysis(self, request: Request) -> Response:
        replay_hash = request.match_info.get("hash", "")

        request_content = await request.json()

        # Do a sanity check for non-corrupt data
        if replay_hash and request_content.get("hash", "") == replay_hash:
            await self.loop.run_in_executor(None, self.db.remove, Query().hash == replay_hash)
            await self.loop.run_in_executor(None, self.db.insert, request_content)
            analysis_url = urllib.parse.urljoin(str(request.url), "../analysis.html?hash=" + replay_hash)
            return json_response({"url": analysis_url})
        else:
            return json_response({}, status=400)

    async def show_analysis_data(self, request: Request) -> Response:
        replay_hash = request.match_info.get("hash", "")

        query = Query().hash == replay_hash
        query_result = await self.loop.run_in_executor(None, self.db.get, query)

        if query_result:
            return json_response(query_result)
        else:
            return json_response({"error": "Error loading analysis."})

