# returns the first n Fibonacci numbers
def first_n(n):
if n == 0 or n == 1:
    return [0] * (n+2)

else:
    fib = [0, 1]
    for i in range(2,n+1):
        fib.append(fib[i-1]+fib[i-2])

    return fib[:n]

