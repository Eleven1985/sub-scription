import base64
import json
import logging
import time
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_subscription():
    try:
        with open('filtered_nodes.json', 'r') as f:
            nodes = json.load(f)
    except FileNotFoundError:
        logging.error("filtered_nodes.json not found")
        return False
    
    if not nodes:
        logging.error("No valid nodes available for subscription")
        return False
    
    # 选择延迟最低的100个节点
    top_nodes = sorted(nodes, key=lambda x: x['latency'])[:100]
    
    # 生成订阅内容
    subscription_content = "\n".join([node['raw'] for node in top_nodes])
    
    # Base64编码
    encoded_content = base64.b64encode(subscription_content.encode()).decode()
    
    # 写入文件
    with open('subscription.txt', 'w') as f:
        f.write(encoded_content)
    
    logging.info(f"Generated subscription with {len(top_nodes)} valid nodes")
    
    # 生成节点质量报告
    generate_report(nodes[:100])  # 报告最快的100个节点
    
    return True

def generate_report(nodes):
    """生成节点质量报告"""
    from datetime import datetime
    
    report = "# V2Ray 节点质量报告\n\n"
    report += f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += "| 协议 | 主机 | 端口 | 延迟(ms) | 质量评级 |\n"
    report += "|------|------|------|----------|----------|\n"
    
    # 计算质量评级
    min_latency = min(node['latency'] for node in nodes)
    max_latency = max(node['latency'] for node in nodes)
    
    for node in nodes:
        latency = node['latency']
        
        # 质量评级算法
        if latency < 100:
            quality = "⭐️⭐️⭐️⭐️⭐️"
        elif latency < 200:
            quality = "⭐️⭐️⭐️⭐️"
        elif latency < 300:
            quality = "⭐️⭐️⭐️"
        elif latency < 500:
            quality = "⭐️⭐️"
        else:
            quality = "⭐️"
        
        report += f"| {node['protocol']} | {node['host']} | {node['port']} | {latency:.2f} | {quality} |\n"
    
    with open('README.md', 'w') as f:
        f.write(report)
    
    logging.info("Generated node quality report")

if __name__ == "__main__":
    generate_subscription()
