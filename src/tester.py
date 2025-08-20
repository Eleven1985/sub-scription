import asyncio, aiohttp, json, logging

TEST_URL = "http://www.gstatic.com/generate_204"
TIMEOUT = 3  # 严格超时控制
MAX_CONCURRENT = 15  # 防资源耗尽

async def test_node(session, node):
    """双重验证：TCP端口+HTTP延迟"""
    try:
        # 1. TCP端口验证
        if not await tcp_check(node['host'], int(node['port'])):
            return -1, False
        
        # 2. HTTP真实延迟测试
        start = time.time()
        async with session.get(TEST_URL, timeout=TIMEOUT) as res:
            if res.status == 204:
                latency = (time.time() - start) * 1000
                return latency, latency > 0  # 返回延迟和有效性
    except Exception:
        return -1, False

async def tcp_check(host, port):
    """验证端口可达性"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=2
        )
        writer.close()
        return True
    except:
        return False

async def main():
    # ...加载节点数据...
    results = []
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)  # 并发控制
        
        async def run_test(node):
            async with semaphore:
                return await test_node(session, node)
        
        tasks = [run_test(node) for node in nodes[:300]]  # 限300节点防超时
        results = await asyncio.gather(*tasks)
    
    # 标记节点有效性
    for i, (latency, valid) in enumerate(results):
        nodes[i]['latency'] = latency
        nodes[i]['valid'] = valid
