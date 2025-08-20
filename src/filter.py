import json
import logging
import socket
import time
import concurrent.futures

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_port(host, port, timeout=3):
    """检查端口是否可达"""
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except:
        return False

def check_http(host, port, timeout=3):
    """检查HTTP服务是否可用"""
    try:
        start = time.time()
        # 模拟HTTP请求
        socket.create_connection((host, int(port)), timeout=timeout).close()
        return (time.time() - start) * 1000  # 返回延迟
    except:
        return -1  # 表示不可用

def filter_nodes():
    """过滤无效节点（延迟为-1或端口不可达）"""
    try:
        with open('tested_nodes.json', 'r') as f:
            nodes = json.load(f)
    except FileNotFoundError:
        logging.error("tested_nodes.json not found")
        return []
    
    if not nodes:
        logging.warning("No nodes to filter")
        return []
    
    logging.info(f"Filtering {len(nodes)} nodes")
    
    # 第一步：移除延迟为-1的节点
    valid_nodes = [node for node in nodes if node.get('delay', -1) > 0 and node['delay'] != float('inf')]
    
    # 第二步：并发检查端口可达性
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for node in valid_nodes:
            futures.append(executor.submit(
                check_port, 
                node['host'], 
                node['port']
            ))
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            if not future.result():
                valid_nodes[i]['valid'] = False
            else:
                valid_nodes[i]['valid'] = True
    
    # 第三步：检查HTTP服务可用性
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for node in valid_nodes:
            if node['valid']:  # 只检查有效的节点
                futures.append(executor.submit(
                    check_http, 
                    node['host'], 
                    node['port']
                ))
            else:
                futures.append(None)  # 占位
        
        for i, future in enumerate(futures):
            if future:
                result = future.result()
                if result == -1:
                    valid_nodes[i]['valid'] = False
                else:
                    # 更新延迟为更准确的HTTP延迟
                    valid_nodes[i]['delay'] = result
    
    # 过滤出有效的节点
    filtered_nodes = [node for node in valid_nodes if node.get('valid', False)]
    
    logging.info(f"Filtered to {len(filtered_nodes)} valid nodes")
    
    # 保存过滤后的节点
    with open('filtered_nodes.json', 'w') as f:
        json.dump(filtered_nodes, f)
    
    return filtered_nodes

if __name__ == "__main__":
    filter_nodes()
