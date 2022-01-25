import time
import subprocess
import multiprocessing


def git_checkout():
    git_proc = subprocess.check_output(["git", "pull"]).decode("utf-8")
    if git_proc == "Already up to date.\n":
        print(git_proc)
        return False
    else:
        print(git_proc)
        return True


def start_server():
    print("Server starting...")
    server_proc = subprocess.check_output(["python", "main.py"]).decode("utf-8")
    print(server_proc)


start_server_thread = multiprocessing.Process(target=start_server)
git_checkout_thread = multiprocessing.Process(target=git_checkout)
server_status = bool(False)

while True:
    git_checkout_thread.start()
    git_checkout_thread.join()
    print("Attempting to check status.")
    if git_checkout():
        start_server_thread.terminate()
        print("Server killed")
        print("Update found.")
        start_server_thread.start()
        print("Server restarting...")
    else:
        print("No update found.")
        if server_status:
            print("Server already running.")
        else:
            print("Server not running.")
            start_server_thread.start()
            server_status = True
            print("Server restarting...")
    git_checkout_thread.terminate()
    time.sleep(10)
