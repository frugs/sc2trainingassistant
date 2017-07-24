import aiohttp

ADD_REPLAY_ANALYSIS_ENDPOINT = "/add/"


class TrainingAssistantClient:

    def __init__(self, host: str):
        self._add_replay_analysis_endpoint = host + ADD_REPLAY_ANALYSIS_ENDPOINT

    async def upload_replay_analysis(self, replay_analysis: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            url = self._add_replay_analysis_endpoint + replay_analysis["hash"]
            async with session.put(url, json=replay_analysis) as resp:
                return await resp.json()
