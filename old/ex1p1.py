import time

N = 20
count = 1000000


def calculate(number):
    result = 0

    for i in range(1, number):
        result += ((i**2) / (i**3)) * (i + i)

    return result


start = time.time()

for i in range(N):
    calculate(count + i)

end = time.time()

print("Задача последовательно. Время:", end - start, "секунд")
