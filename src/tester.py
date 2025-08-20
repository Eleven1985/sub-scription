# ... 原有代码 ...

def test_nodes():
    # ... 原有代码 ...
    
    # 使用线程池并发测试
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for node in nodes_to_test:
            futures.append(executor.submit(
                tcp_ping, 
                node['host'], 
                node['port']
            ))
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            delay = future.result()
            nodes_to_test[i]['delay'] = delay
            
            # 标记无效节点（延迟为-1）
            if delay == -1:
                nodes_to_test[i]['valid'] = False
            else:
                nodes_to_test[i]['valid'] = True
    
    # 按延迟排序
    tested_nodes = sorted(nodes_to_test, key=lambda x: x['delay'])
    
    # 保存测试结果
    with open('tested_nodes.json', 'w') as f:
        json.dump(tested_nodes, f)
    
    return tested_nodes

# ... 其余代码 ...
