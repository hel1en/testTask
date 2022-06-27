def f(**kwargs):
    print(kwargs)


c = dict(a=1)

if __name__ == '__main__':
    f(**c)
