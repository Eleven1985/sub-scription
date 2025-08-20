import base64, json

def verify_node(node):
    """二次验证节点有效性"""
    # 实现TCP端口检查或HTTP请求验证
    return True  # 简化示例

def generate():
    with open('processed_nodes.json') as f:
        nodes = json.load(f)
    
    valid_nodes = [n for n in nodes if verify_node(n)][:20]
    encoded = base64.b64encode("\n".join(valid_nodes).encode()).decode()
    
    with open('subscription.txt', 'w') as f:
        f.write(encoded)

if __name__ == "__main__":
    generate()
