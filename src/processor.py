def extract_unique_id(node):
    # 支持VMess/VLess/Trojan/Shadowsocks协议
    patterns = {
        "vmess": r"@([\w\.-]+):(\d+)\?",
        "vless": r"@([\w\.-]+):(\d+)#",
        "trojan": r"@([\w\.-]+):(\d+)\?",
        "ss": r"@([\w\.-]+):(\d+)#"
    }
    for proto, pattern in patterns.items():
        if match := re.search(pattern, node):
            return f"{proto}://{match.group(1)}:{match.group(2)}"
    return None  # 无法解析的节点丢弃
