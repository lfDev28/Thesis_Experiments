from celery import Celery
import time

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//', backend='rpc://')


def find_primes_logic(n=500000):
    primes = []
    for num in range(1, n + 1):
        prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                prime = False
                break
        if prime:
            primes.append(num)
    return primes


@app.task
def find_primes(num):
    return find_primes_logic(num)