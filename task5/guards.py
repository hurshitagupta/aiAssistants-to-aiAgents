import time
import functools
import concurrent.futures as cf


def with_retry(attempts: int = 3, base: float = 0.8):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            for i in range(attempts):
                try:
                    return fn(*a, **kw)
                except Exception as exc:
                    if i == attempts - 1:
                        raise
                    print(f"[retry {i+1}/{attempts}] {type(exc).__name__}: {exc}")
                    time.sleep(base * 2 ** i)
        return wrapper
    return deco


def call_with_timeout(fn, kwargs: dict, seconds: float = 5.0) -> str:
    with cf.ThreadPoolExecutor(max_workers=1) as pool:
        fut = pool.submit(fn, **kwargs)
        try:
            return str(fut.result(timeout=seconds))
        except cf.TimeoutError:
            return f"timeout after {seconds}s"