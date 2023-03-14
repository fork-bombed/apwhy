from apwhy.api import Endpoint, Api
from apwhy.recon.files import Wordlist
import apwhy.console.cli as console
import aiohttp
import asyncio
import time


def response_filter(response: aiohttp.ClientResponse) -> bool:
    if response.status == 404 or response.status == 500:
        return False
    return True


async def method_sweep_endpoint(endpoint: Endpoint) -> None:
    sweep_tasks = []
    sweep_tasks.append(await endpoint.post())
    sweep_tasks.append(await endpoint.put())
    sweep_tasks.append(await endpoint.patch())
    sweep_tasks.append(await endpoint.head())
    sweep_tasks.append(await endpoint.delete())
    for response in sweep_tasks:
        await output_response(response)


def index_mismatch(request_path: str, response_path: str) -> bool:
    return request_path == response_path


async def probe_endpoint(endpoint: Endpoint) -> None:
    response = await endpoint.get()
    if response.request_info.url.path != '/':
        await output_response(response)
        # if response_filter(response):
        #     await method_sweep_endpoint(endpoint)


async def output_response(response: aiohttp.ClientResponse) -> None:
    row = [response.request_info.method, response.request_info.url.path, response.status, len(await response.text())]
    if response_filter(response):
        match str(response.status)[0]:
            case "2":
                console.output_row(row, color="light_green")
            case "3":
                console.output_row(row, color="light_blue")
            case "4":
                console.output_row(row, color="light_red")
            case "5":
                console.output_row(row, color="light_yellow")
            case _:
                console.output_row(row)
    else:
        console.output_row(row)
        console.overwrite_last_line()


async def enumerate(api: Api, wordlist_path: str, limit: int) -> None:
    wordlist = Wordlist(wordlist_path)
    wordlist.read()
    connector = aiohttp.TCPConnector(force_close=True, limit=limit)
    async with aiohttp.ClientSession(connector=connector) as session:
        console.output(f"Enumerating {wordlist.get_size()} endpoints...\n")
        header = ["METHOD", "PATH", "STATUS", "SIZE"]
        console.output_row(header)
        probe_tasks = []
        for word in wordlist.get_words():
            endpoint = Endpoint(api, session, word)
            task = asyncio.create_task(probe_endpoint(endpoint))
            probe_tasks.append(task)
        start_time = time.time()
        await asyncio.gather(*probe_tasks)
        elapsed_time = time.time() - start_time
    console.output(
        f"\nEnumerated {wordlist.get_size()} endpoint(s) in {elapsed_time:.2f} seconds"
    )


def run(api: Api, wordlist_path: str, limit: int) -> None:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(enumerate(api, wordlist_path, limit))
