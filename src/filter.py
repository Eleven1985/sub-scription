import json, logging

logging.basicConfig(level=logging.INFO)

def filter_nodes():
    with open('tested_nodes.json') as f:
        nodes = json.load(f)
    
    # 关键修复：双重验证有效性
    valid_nodes = [
        node for node in nodes 
        if node.get('valid') is True and node.get('latency', -1) > 0
    ]
    
    # 按延迟排序取最快100个
    sorted_nodes = sorted(valid_nodes, key=lambda x: x['latency'])[:100]
    
    with open('filtered_nodes.json', 'w') as f:
        json.dump(sorted_nodes, f)
