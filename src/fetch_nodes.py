import aiohttp, asyncio, base64

async def fetch(url, max_retry=3):
    async with aiohttp.ClientSession() as session:
        for _ in range(max_retry):
            try:
                async with session.get(url, timeout=10) as res:
                    content = await res.text()
                    return content if not url.endswith('.txt') else base64.b64decode(content).decode()
            except Exception:
                await asyncio.sleep(2)
        return ""  # 失败返回空
