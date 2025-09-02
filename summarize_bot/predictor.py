from abc import ABC, abstractmethod
import aiohttp


class Predictor(ABC):
    model_name: str

    def __init__(self):
        pass

    @abstractmethod
    async def predict(self, text: str) -> str:
        pass

    @property
    async def modelinfo(self) -> dict[str, str]:
        api_url = f"https://huggingface.co/api/models/{self.model_name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=api_url, raise_for_status=True) as response:
                return await response.json()
