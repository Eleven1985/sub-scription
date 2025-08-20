import socket
import time
import json
import logging
import concurrent.futures
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def tcp_ping(host, port, timeout=3):
    """TCP连接测试延迟"""
    start = time.time()
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            delay = (time.time() - start) * 1000  # 毫秒
            return delay
    except Exception as e:
        logging.debug(f"TCP ping failed for {host}:{port}: {str(e)}")
        return float('inf')  # 表示不可达

def test_nodes():
    try:
        with open('processed_nodes.json', 'r') as f:
            nodes = json.load(f)
    except FileNotFoundError:
        logging.error("processed_nodes.json not found")
        return []
    
    if not nodes:
        logging.warning("No nodes to test")
        return []
    
    # 限制最大测试节点数（防止超时）
    max_test_nodes = min(200, len(nodes))
    nodes_to_test = nodes[:max_test_nodes]
    
    logging.info(f"Testing {len(nodes_to_test)} nodes")
    
    # 使用线程池并发测试
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for node in nodes_to_test:
            futures.append(executor.submit(
                tcp_ping, 
                node['host'], 
                node['port']
            ))
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            nodes_to_test[i]['delay'] = future.result()
    
    # 按延迟排序
    tested_nodes = sorted(nodes_to_test, key=lambda x: x['delay'])
    
    # 保存测试结果
    with open('tested_nodes.json', 'w') as f:
        json.dump(tested_nodes, f)
    
    return tested_nodes

if __name__ == "__main__":
    test_nodes()
