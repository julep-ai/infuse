from ..models import ExecuteIntegrationArguments, ExecuteIntegrationSetup
from .integrations.hacker_news import hacker_news
from .integrations.weather import weather
from .integrations.wikipedia import wikipedia
from .integrations.spider import spider

async def execute_integration(
    provider: str,
    setup: ExecuteIntegrationSetup | None,
    arguments: ExecuteIntegrationArguments,
) -> str:
    match provider:
        case "wikipedia":
            return await wikipedia(arguments=arguments)
        case "weather":
            return await weather(setup=setup, arguments=arguments)
        case "hacker_news":
            return await hacker_news(arguments=arguments)
        case "spider":
            return await spider(setup=setup, arguments=arguments)
        case _:
            raise ValueError(f"Unknown integration: {provider}")
