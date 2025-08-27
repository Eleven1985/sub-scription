import re
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_node_info(node):
    """解析各种协议节点信息"""
    protocols = {
        'vmess': r'vmess://[^@]+@([^:]+):(\d+)\?',
        'vless': r'vless://[^@]+@([^:]+):(\d+)[#?]',
        'trojan': r'trojan://[^@]+@([^:]+):(\d+)\?',
        'ss': r'ss://[^@]+@([^:]+):(\d+)[#?]',
        'tuic': r'tuic://[^@]+@([^:]+):(\d+)\?',
        'hysteria': r'hysteria://[^@]+@([^:]+):(\d+)\?'
    }
    
    for proto, pattern in protocols.items():
        match = re.search(pattern, node)
        if match:
            host = match.group(1)
            port = match.group(2)
            return {
                'protocol': proto,
                'host': host,
                'port': port,
                'raw': node,
                'key': f"{proto}://{host}:{port}"
            }
    
    logging.warning(f"Unrecognized node format: {node[:100]}...")
    return None

def process_nodes():
    try:
        with open('raw_nodes.txt', 'r') as f:
            raw_nodes = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        logging.error("raw_nodes.txt not found")
        return []
    
    if not raw_nodes:
        logging.warning("No nodes found in raw_nodes.txt")
        return []
    
    processed_nodes = []
    unique_keys = set()
    
    for node in raw_nodes:
        info = extract_node_info(node)
        if info and info['key'] not in unique_keys:
            unique_keys.add(info['key'])
            processed_nodes.append(info)
    
    logging.info(f"Processed {len(processed_nodes)} unique nodes")
    
    # 保存处理后的节点信息
    with open('processed_nodes.json', 'w') as f:
        json.dump(processed_nodes, f)
    
    return processed_nodes

if __name__ == "__main__":
    process_nodes()
