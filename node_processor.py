import os, re, requests, base64
import pandas as pd
from datetime import datetime

# 1. 抓取节点数据
def fetch_nodes():
    urls = os.environ['SOURCE_URLS'].split()
    all_nodes = []
    
    for url in urls:
        try:
            res = requests.get(url, timeout=10)
            if url.endswith('.txt'):
                # 处理Base64编码订阅
                decoded = base64.b64decode(res.text).decode('utf-8')
                nodes = [n for n in decoded.splitlines() if n.startswith('vmess://')]
            else:
                nodes = [n.strip() for n in res.text.splitlines() if n]
            all_nodes.extend(nodes)
        except Exception as e:
            print(f"Failed {url}: {str(e)}")
    return list(set(all_nodes))  # 初步去重

# 2. 节点去重与解析
def deduplicate(nodes):
    unique = {}
    for node in nodes:
        try:
            # 提取关键标识符（地址+端口）
            addr_port = re.search(r"@(.+?):(\d+)", node).groups()
            key = f"{addr_port[0]}:{addr_port[1]}"
            unique[key] = node
        except: 
            continue
    return list(unique.values())

# 3. 速度测试（Ping延迟）
def test_speed(nodes, max_nodes=20):
    results = []
    for node in nodes[:100]:  # 限制测试数量
        addr = re.search(r"@(.+?):", node).group(1)
        start = datetime.now()
        try:
            requests.get(f"http://{addr}", timeout=3)
            delay = (datetime.now() - start).total_seconds() * 1000  # 毫秒
            results.append((node, delay))
        except:
            results.append((node, 9999))  # 超时标记
    
    # 按延迟排序取最优
    df = pd.DataFrame(results, columns=['node', 'delay'])
    df = df.sort_values(by='delay').head(max_nodes)
    return df['node'].tolist()

# 4. 生成订阅文件
def generate_subscription(nodes):
    encoded = base64.b64encode("\n".join(nodes).encode()).decode()
    with open('subscription.txt', 'w') as f:
        f.write(encoded)
    return encoded

if __name__ == "__main__":
    nodes = fetch_nodes()
    nodes = deduplicate(nodes)
    top_nodes = test_speed(nodes)
    generate_subscription(top_nodes)
