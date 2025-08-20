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
    
    # 筛选5星节点（延迟<100ms）
    five_star_nodes = [node for node in nodes if node.get('latency', 999) < 100]
    
    # 最多保留100个5星节点
    top_nodes = five_star_nodes[:100]
    
    # 生成订阅内容
    subscription_content = "\n".join([node['raw'] for node in top_nodes])
    
    # Base64编码
    encoded_content = base64.b64encode(subscription_content.encode()).decode()
    
    # 写入订阅文件
    with open('subscription.txt', 'w') as f:
        f.write(encoded_content)
    
    logging.info(f"Generated subscription with {len(top_nodes)} 5-star nodes")
    
    # 生成节点质量报告（仅包含5星节点）
    generate_report(top_nodes)
    
    return True

def generate_report(nodes):
    """生成仅包含5星节点的质量报告"""
    from datetime import datetime
    
    report = "# V2Ray 节点质量报告（5星节点）\n\n"
    report += f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += f"**节点总数**: {len(nodes)}\n\n"
    report += "| 序号 | 协议 | 主机 | 端口 | 延迟(ms) | 节点链接 |\n"
    report += "|------|------|------|------|----------|----------|\n"
    
    for i, node in enumerate(nodes, 1):
        latency = node['latency']
        host = node['host']
        port = node['port']
        protocol = node['protocol']
        raw_link = node['raw'][:60] + "..."  # 截取部分节点链接
        
        report += f"| {i} | {protocol} | {host} | {port} | {latency:.2f} | `{raw_link}` |\n"
    
    with open('REPORT.md', 'w') as f:
        f.write(report)
    
    logging.info(f"Generated quality report with {len(nodes)} 5-star nodes")

if __name__ == "__main__":
    generate_subscription()
