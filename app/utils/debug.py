from functools import wraps

def print_ret(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(f'ret: {ret}')
        return ret
        
    return wrapper
