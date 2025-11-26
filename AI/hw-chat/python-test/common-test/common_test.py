

def outer_function():
    x = 10
    def inner_function():
        nonlocal x
        x = 20
        print(f'inner_function:{x}')
    inner_function()
    print(x)


if __name__ == '__main__':
    outer_function()