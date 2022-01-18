import multiprocessing
import time
import subprocess
import asyncio


# import git


# git_module = git.cmd.Git(".git")
async def git_checkout():
    git_proc = subprocess.check_output(['git', 'pull']).decode('utf-8')
    if git_proc == "Already up to date.\n":
        print(git_proc)
        return False
    else:
        print(git_proc)
        return True


asyncio.run(git_checkout())

server_status = bool(False)

async def start_server():
    print("Starting server")
    server_proc = subprocess.Popen(['python3', 'main.py'])
    server_out = server_proc.communicate()
    server_status = bool(True)
    print(server_out)
    return server_proc

asyncio.run(start_server())
server_proc = start_server()

while True:
    git_status = asyncio.run(git_checkout())
    print("Attempting to check status.")
    if git_status:
        print("Update found.")
        if server_status:
            print("Server already running.")
            server_proc.terminate()
            server_status = bool(False)
        else:
            print("Server not running.")
        asyncio.run(start_server())
        print("Server restarted.")
    else:
        print("No update found.")
        if server_status:
            print("Server already running.")
        else:
            print("Server not running.")
            asyncio.run(start_server())
            print("Server restarted.")
    time.sleep(60)
