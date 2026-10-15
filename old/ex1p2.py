import time
import threading


N = 20
count = 1000000


def calculate(number):
    result = 0

    for i in range(1, number):
        result += ((i**2) / (i**3)) * (i + i)


threads = []

start = time.time()

for i in range(N):
    thread = threading.Thread(target=calculate, args=(count + i,))

    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()

end = time.time()


print("Задача потоки. Время выполнения:", end - start, "секунд")
