import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def filter_nodes():
    """过滤节点并保留最快的100个节点"""
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
    
    # 按延迟排序
    sorted_nodes = sorted(nodes, key=lambda x: x['latency'])
    
    # 保留最快的100个节点
    top_nodes = sorted_nodes[:min(100, len(sorted_nodes))]
    
    logging.info(f"Filtered to {len(top_nodes)} fastest nodes")
    
    # 保存过滤后的节点
    with open('filtered_nodes.json', 'w') as f:
        json.dump(top_nodes, f)
    
    return top_nodes

if __name__ == "__main__":
    filter_nodes()
