import asyncio, aiohttp, json, time

TEST_URL = "http://www.gstatic.com/generate_204"
TIMEOUT = 5

async def test_node(session, node):
    try:
        start = time.time()
        async with session.get(TEST_URL, proxy=f"http://{node['host']}:{node['port']}", timeout=TIMEOUT) as res:
            if res.status == 204:
                return (time.time() - start) * 1000  # 返回真实延迟
    except:
        return -1  # 标记失败节点

async def main():
    with open('processed_nodes.json') as f:
        nodes = json.load(f)
    
    async with aiohttp.ClientSession() as session:
        tasks = [test_node(session, node) for node in nodes[:300]]  # 限制测试数量
        delays = await asyncio.gather(*tasks)
        
    for i, node in enumerate(nodes[:300]):
        node['latency'] = delays[i]
        node['valid'] = delays[i] > 0  # 有效性标记
    
    with open('tested_nodes.json', 'w') as f:
        json.dump(nodes, f)

if __name__ == "__main__":
    asyncio.run(main())
