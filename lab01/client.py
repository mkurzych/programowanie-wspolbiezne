import time

r = ''
n = input("Input a number: ")

with open("dane.txt", "w") as data:
    data.write(n)

while r == '':
    with open("wyniki.txt", "r") as results:
        r = results.read()
        time.sleep(0.25)

print('Result:', r)

with open("wyniki.txt", "w") as results:
    results.write("")

with open("dane.txt", "w") as data:
    data.write("")
