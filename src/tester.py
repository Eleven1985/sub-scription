import json
import logging
import asyncio
import aiohttp
import time
import socket
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TEST_URL = "http://www.gstatic.com/generate_204"  # Google的204响应服务
TIMEOUT = 10  # 超时时间（秒）
MAX_CONCURRENT = 100  # 最大并发数

async def test_single_node(session, node):
    """测试单个节点的实际速度"""
    try:
        # 解析节点信息
        host = node['host']
        port = int(node['port'])
        protocol = node['protocol']
        
        # 创建代理连接
        connector = None
        proxy_url = None
        
        if protocol in ['http', 'https']:
            proxy_url = f"http://{host}:{port}"
        elif protocol == 'socks5':
            proxy_url = f"socks5://{host}:{port}"
        else:
            # 对于其他协议，使用TCP连接测试
            return await tcp_ping(host, port)
        
        # 使用代理测试实际速度
        start_time = time.time()
        async with session.get(TEST_URL, proxy=proxy_url, timeout=TIMEOUT) as response:
            if response.status == 204:
                latency = (time.time() - start_time) * 2000  # 毫秒
                return latency
            else:
                logging.warning(f"Unexpected status {response.status} for {host}:{port}")
                return -1
    except asyncio.TimeoutError:
        logging.debug(f"Timeout for {host}:{port}")
        return -1
    except Exception as e:
        logging.debug(f"Error testing {host}:{port}: {str(e)}")
        return -1

async def tcp_ping(host, port):
    """TCP连接测试"""
    try:
        start_time = time.time()
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=TIMEOUT
        )
        latency = (time.time() - start_time) * 2000
        writer.close()
        await writer.wait_closed()
        return latency
    except:
        return -1

async def test_nodes(nodes):
    """并发测试所有节点"""
    results = []
    
    # 创建HTTP会话
    async with aiohttp.ClientSession() as session:
        tasks = []
        for node in nodes:
            tasks.append(test_single_node(session, node))
        
        # 分批测试，避免并发过高
        for i in range(0, len(tasks), MAX_CONCURRENT):
            batch = tasks[i:i+MAX_CONCURRENT]
            batch_results = await asyncio.gather(*batch)
            results.extend(batch_results)
    
    return results

def main():
    try:
        with open('processed_nodes.json', 'r') as f:
            nodes = json.load(f)
    except FileNotFoundError:
        logging.error("processed_nodes.json not found")
        return []
    
    if not nodes:
        logging.warning("No nodes to test")
        return []
    
    # 限制最大测试节点数
    max_test_nodes = min(2000, len(nodes))
    nodes_to_test = nodes[:max_test_nodes]
    
    logging.info(f"Testing {len(nodes_to_test)} nodes")
    
    # 运行异步测试
    loop = asyncio.get_event_loop()
    latencies = loop.run_until_complete(test_nodes(nodes_to_test))
    
    # 更新节点延迟信息
    for i, node in enumerate(nodes_to_test):
        node['latency'] = latencies[i]
        node['valid'] = latencies[i] > 0
    
    # 保存测试结果
    with open('tested_nodes.json', 'w') as f:
        json.dump(nodes_to_test, f)
    
    logging.info(f"Completed testing {len(nodes_to_test)} nodes")
    return nodes_to_test

if __name__ == "__main__":
    main()
