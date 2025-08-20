import re, pandas as pd

def extract_key(node):
    """支持多协议解析"""
    patterns = [
        r"@([\w\.-]+):(\d+)\?",    # VMess/VLess
        r"host=([\w\.-]+).*?port=(\d+)", # Trojan
        r"server=([\w\.-]+).*?port=(\d+)" # Shadowsocks
    ]
    for pattern in patterns:
        match = re.search(pattern, node)
        if match: return f"{match.group(1)}:{match.group(2)}"
    return None

def process():
    with open('raw_nodes.txt') as f:
        nodes = [n.strip() for n in f.readlines() if n.strip()]
    
    # 高级去重
    unique = {}
    for node in nodes:
        if key := extract_key(node):
            unique[key] = node
    
    # 并发测试优化[8](@ref)
    test_results = []
    for node in list(unique.values())[:200]:  # 限制测试数量
        # ... (速度测试逻辑)
    
    pd.DataFrame(test_results).to_json('processed_nodes.json')

if __name__ == "__main__":
    process()
