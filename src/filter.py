def filter_nodes():
    with open('tested_nodes.json') as f:
        nodes = json.load(f)
    
    # 四级过滤链
    valid_nodes = [
        node for node in nodes 
        if node['valid'] is True               # 有效性标记
        and node['latency'] > 0                 # 排除-1值
        and node['latency'] < 500              # 排除高延迟
        and isinstance(node['latency'], float)  # 类型校验
    ]
    
    # 按延迟排序取最快100个
    sorted_nodes = sorted(valid_nodes, key=lambda x: x['latency'])[:100]
    
    # 空节点熔断
    if not sorted_nodes:
        logging.critical("⚠️ 无有效节点，启用历史缓存")
        shutil.copy('last_valid_nodes.json', 'filtered_nodes.json')
    else:
        with open('filtered_nodes.json', 'w') as f:
            json.dump(sorted_nodes, f)
        # 备份有效节点
        shutil.copy('filtered_nodes.json', 'last_valid_nodes.json')
