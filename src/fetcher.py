import os
import asyncio
import aiohttp
import base64
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_url(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                content = await response.text()
                if url.endswith('.txt'):
                    # 处理Base64编码订阅
                    try:
                        return base64.b64decode(content).decode('utf-8')
                    except:
                        return content
                return content
            else:
                logging.warning(f"Failed to fetch {url}: Status {response.status}")
                return ""
    except Exception as e:
        logging.error(f"Error fetching {url}: {str(e)}")
        return ""

async def main():
    urls = os.environ.get('SOURCE_URLS', '').split()
    if not urls:
        logging.error("No source URLs provided")
        return
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        valid_results = [r for r in results if r]
        if not valid_results:
            logging.error("All fetch attempts failed")
            return
        
        with open('raw_nodes.txt', 'w') as f:
            for content in valid_results:
                f.write(content + "\n")
        
        logging.info(f"Successfully fetched {len(valid_results)} sources")

if __name__ == "__main__":
    asyncio.run(main())
