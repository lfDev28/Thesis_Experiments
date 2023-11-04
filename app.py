import psutil
import time
from concurrent.futures import ThreadPoolExecutor
from tasks import find_primes

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def count_primes(num):
    return sum(1 for i in range(2, num) if is_prime(i))

def threaded_primes():
    with ThreadPoolExecutor() as executor:
        # Splitting the workload into 10 chunks
        futures = [executor.submit(count_primes, 100000) for _ in range(10)]
    return [f.result() for f in futures]

def queue_primes():
    results = [find_primes.delay(100000) for _ in range(10)]
    return [res.get() for res in results]

def measure(func):
    initial_cpu = psutil.cpu_percent(1)
    initial_ram = psutil.virtual_memory().percent

    start_time = time.time()
    func()
    execution_time = time.time() - start_time

    final_cpu = psutil.cpu_percent(1)
    final_ram = psutil.virtual_memory().percent

    return initial_cpu, final_cpu, initial_ram, final_ram, execution_time

def average_metrics(metrics):
    return tuple(sum(metric) / len(metric) for metric in zip(*metrics))

if __name__ == "__main__":
    runs = 10

    threaded_metrics = []
    queue_metrics = []

    for _ in range(runs):
        threaded_metrics.append(measure(threaded_primes))
        queue_metrics.append(measure(queue_primes))

    avg_threaded = average_metrics(threaded_metrics)
    avg_queue = average_metrics(queue_metrics)

    print("---- Average Metrics for Multithreading ----")
    print(f"Initial CPU usage: {avg_threaded[0]:.2f}%")
    print(f"Final CPU usage: {avg_threaded[1]:.2f}%")
    print(f"Initial RAM usage: {avg_threaded[2]:.2f}%")
    print(f"Final RAM usage: {avg_threaded[3]:.2f}%")
    print(f"Execution Time: {avg_threaded[4]:.2f} seconds\n")

    print("---- Average Metrics for Queue (Celery) ----")
    print(f"Initial CPU usage: {avg_queue[0]:.2f}%")
    print(f"Final CPU usage: {avg_queue[1]:.2f}%")
    print(f"Initial RAM usage: {avg_queue[2]:.2f}%")
    print(f"Final RAM usage: {avg_queue[3]:.2f}%")
    print(f"Execution Time: {avg_queue[4]:.2f} seconds")
