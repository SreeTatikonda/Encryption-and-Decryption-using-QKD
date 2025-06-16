import time

def log_latency(tag="Operation"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"[{tag}] Latency: {round(end - start, 5)} sec")
            return result
        return wrapper
    return decorator
