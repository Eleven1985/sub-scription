import base64
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_subscription():
    try:
        with open('tested_nodes.json', 'r') as f:
            nodes = json.load(f)
    except FileNotFoundError:
        logging.error("tested_nodes.json not found")
        return False
    
    if not nodes:
        logging.error("No nodes available for subscription")
        return False
    
    # 选择延迟最低的20个节点
    top_nodes = [node['raw'] for node in nodes[:20]]
    
    # 生成订阅内容
    subscription_content = "\n".join(top_nodes)
    
    # Base64编码
    encoded_content = base64.b64encode(subscription_content.encode()).decode()
    
    # 写入文件
    with open('subscription.txt', 'w') as f:
        f.write(encoded_content)
    
    logging.info(f"Generated subscription with {len(top_nodes)} nodes")
    return True

if __name__ == "__main__":
    generate_subscription()
