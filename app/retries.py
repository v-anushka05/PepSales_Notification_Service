import time

def retry_with_backoff(func, args, max_retries=3, delay=3):
    tries = 0
    while tries < max_retries:
        try:
            return func(*args)
        except Exception as e:
            tries += 1
            if tries == max_retries:
                raise e
            time.sleep(delay * tries)