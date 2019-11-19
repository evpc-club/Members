
def ask():
    name = input("What is your name")
    age = input("How old are you")
    ask = input("Are your parents with you y/n")
    while ask != ("y" or "n"):
        ask = input("Are your parents with you y/n")
    if ask == "n":
        print("nevermind")
    elif ask == "y":
        print("test")

ask()


