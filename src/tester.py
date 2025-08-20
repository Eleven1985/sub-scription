import socket, time

def tcp_ping(host, port, timeout=3):
    start = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return (time.time() - start) * 1000  # 返回毫秒延迟
    except:
        return 9999  # 超时标记
