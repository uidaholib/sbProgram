
def main():
    print("main")
    color = "green"
    print("One layer or two?")
    answer = input("> ").lower()
    if "1" in answer:
        first(color)
    elif "2" in answer:
        first_second(color)

    print("final color:")
    print(color)


def first(color):
    print("first")
    color = "red"
    return color

def first_second(color):
    print("first_second")
    second(color)

def second(color):
    print("second")
    color = "blue"
    return color





if __name__ == '__main__':
    main()
