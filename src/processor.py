import re, json, logging

logging.basicConfig(level=logging.INFO)
PROTOCOL_PATTERNS = {
    'vmess': r'@([\w\.-]+):(\d+)\?',
    'vless': r'@([\w\.-]+):(\d+)[#?]',
    'trojan': r'@([\w\.-]+):(\d+)\?',
    'ss': r'@([\w\.-]+):(\d+)[#?]'
}

def extract_node_info(node):
    for proto, pattern in PROTOCOL_PATTERNS.items():
        if match := re.search(pattern, node):
            return {
                'protocol': proto,
                'host': match.group(1),
                'port': match.group(2),
                'raw': node,
                'key': f"{proto}://{match.group(1)}:{match.group(2)}"
            }
    return None

def process():
    with open('raw_nodes.txt') as f:
        nodes = [n.strip() for n in f if n.strip()]
    
    unique_nodes = {}
    for node in nodes:
        if info := extract_node_info(node):
            unique_nodes[info['key']] = info
    
    with open('processed_nodes.json', 'w') as f:
        json.dump(list(unique_nodes.values()), f)
