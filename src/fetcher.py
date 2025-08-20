import asyncio, aiohttp, base64, os

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as res:
                content = await res.text()
                return content if not url.endswith('.txt') else base64.b64decode(content).decode()
        except:
            return ""

async def main():
    urls = os.environ['SOURCE_URLS'].split()
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    with open('raw_nodes.txt', 'w') as f:
        for content in results:
            if content: f.write(content + "\n")

if __name__ == "__main__":
    asyncio.run(main())
