import base64, json, time, logging

logging.basicConfig(level=logging.INFO)

def generate():
    with open('filtered_nodes.json') as f:
        nodes = json.load(f)
    
    # 只保留5星节点（延迟<100ms）
    five_star_nodes = [node for node in nodes if node['latency'] < 100][:20]
    
    # 生成订阅
    sub_content = "\n".join([n['raw'] for n in five_star_nodes])
    encoded = base64.b64encode(sub_content.encode()).decode()
    with open('subscription.txt', 'w') as f:
        f.write(encoded)
    
    # 生成带节点链接的报告
    report = "| 序号 | 协议 | 主机 | 端口 | 延迟 | 节点片段 |\n|-----|------|------|-----|-------|--------|\n"
    for i, node in enumerate(five_star_nodes, 1):
        report += f"| {i} | {node['protocol']} | {node['host']} | {node['port']} | {node['latency']:.2f}ms | `{node['raw'][:30]}...` |\n"
    
    with open('REPORT.md', 'w') as f:
        f.write(f"# 5星节点报告\n更新于: {time.ctime()}\n\n{report}")

if __name__ == "__main__":
    generate()
