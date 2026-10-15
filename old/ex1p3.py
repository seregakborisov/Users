import time
import multiprocessing
import os


N = os.cpu_count()
NUMBER = 5000000


def calculate(number):
    result = 0

    for i in range(1, number):
        result += ((i**2) / (i**3)) * (i + i)


if __name__ == "main":
    processes = []

    start = time.perf_counter()

    for i in range(N):
        process = multiprocessing.Process(target=calculate, args=(NUMBER + i,))

        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end = time.perf_counter()

    print("Процессы")
    print("Количество процессов:", N)
    print("Количество ядер:", N)
    print("Время:", end - start, "секунд")
