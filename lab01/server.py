import time

d = ''

while True:
    with open("dane.txt", "r") as data:
        d = data.read()
        if d != '':
            with open("wyniki.txt", "w") as results:
                results.write(str(int(d) ** 2))
        print(d)
        time.sleep(0.25)


