import re

import aiohttp
import pkg_resources
from aiohttp.web import Application, Response, Request, HTTPFound

SUCCESS_CODE_PATTERN = re.compile(r"^2\d\d$")


def is_success(response: Response) -> bool:
    return bool(SUCCESS_CODE_PATTERN.search(str(response.status)))


def has_multipart_content(request: Request) -> bool:
    return request.content_type.startswith("multipart/")


class ReplayUploaderApplication(Application):

    def __init__(
            self,
            analyse_replay_endpoint: str,
            add_replay_analysis_endpoint: str,
            show_replay_analysis_endpoint: str):

        Application.__init__(self)

        self.router.add_post("/upload", self.upload_replay)
        self.router.add_static('/', pkg_resources.resource_filename(__name__, "public"))

        self.analyse_replay_endpoint = analyse_replay_endpoint
        self.add_replay_analysis_endpoint = add_replay_analysis_endpoint
        self.show_replay_analysis_endpoint = show_replay_analysis_endpoint

    async def upload_replay(self, request: Request) -> Response:

        async with aiohttp.ClientSession() as session:

            if has_multipart_content(request):
                reader = await request.multipart()
                data = await reader.next()
            else:
                data = request.content

            if data is not None:
                async with session.post(self.analyse_replay_endpoint, data=data) as resp1:
                    if is_success(resp1):
                        replay_analysis = await resp1.json()

                        replay_hash = replay_analysis.get("hash", "")

                        if replay_hash:
                            url = self.add_replay_analysis_endpoint + replay_hash
                            async with session.put(url, json=replay_analysis) as resp2:
                                if is_success(resp2):
                                    return HTTPFound(self.show_replay_analysis_endpoint + replay_hash)

        return HTTPFound("index.html?error=true")
