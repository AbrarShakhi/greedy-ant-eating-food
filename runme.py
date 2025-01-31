from sys import exit

try:
    import src.main
except:
    print("src/main.py does not exists.")
    exit(1)


if __name__ == "__main__":
    src.main.main("src")
