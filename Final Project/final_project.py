import time

def countdown(usermins):
    for remaining in range(usermins, -1, -1):
        mins, secs = divmod(remaining, 60 * usermins)
        print(f"{mins:02d}:{secs:02d}", end="\r", flush=True)
        if remaining > 0:
            time.sleep(1)
    print(f"{seconds} seconds have passed!")



def main():
    usermins = int(input("How many minutes do you want your timer to go for?"))
    countdown(usermins)
if __name__ == "__main__":
    main()