def generate():
    with open('filtered_nodes.json') as f:
        nodes = json.load(f)
    
    # 动态配额：优先取5星(<100ms)，不足时补4星(<200ms)
    five_star = [n for n in nodes if n['latency'] < 100]
    four_star = [n for n in nodes if 100 <= n['latency'] < 200]
    top_nodes = (five_star + four_star)[:100]  # 合并取前100
    
    # 生成带评级的报告
    report = "| 主机 | 端口 | 协议 | 延迟(ms) | 评级 |\n"
    report += "|------|------|------|----------|------|\n"
    for node in top_nodes:
        rating = "⭐️⭐️⭐️⭐️⭐️" if node['latency'] < 100 else "⭐️⭐️⭐️⭐️"
        report += f"| {node['host']} | {node['port']} | {node['protocol']} | {node['latency']:.2f} | {rating} |\n"
    
    # 写入订阅文件（仅包含原始节点数据）
    raw_links = "\n".join([n['raw'] for n in top_nodes])
    encoded = base64.b64encode(raw_links.encode()).decode()
    with open('subscription.txt', 'w') as f:
        f.write(encoded)
