import multiprocessing
import time
import subprocess
import asyncio


# import git


# git_module = git.cmd.Git(".git")
async def git_checkout():
    git_proc = subprocess.check_output(["git", "pull"]).decode("utf-8")
    if git_proc == "Already up to date.\n":
        print(git_proc)
        return False
    else:
        print(git_proc)
        return True


asyncio.run(git_checkout())


async def git_checkout_loop():
    while True:
        await asyncio.sleep(60)
        await git_checkout()


server_status = bool(False)


async def start_server():
    print("Starting server")
    server_status = bool(True)
    server_out = subprocess.check_output(["python", "main.py"]).decode("utf-8")
    print(server_out)


"""
while True:
    git_status = asyncio.run(git_checkout())
    print("Attempting to check status.")
    if git_status:
        print("Update found.")
        if server_status:
            print("Server already running.")
            asyncio.cancel(start_server())
            server_status = bool(False)
        else:
            print("Server not running.")
        asyncio.loop.call_soon(asyncio.run(start_server()))
        print("Server restarted.")
    else:
        print("No update found.")
        if server_status:
            print("Server already running.")
        else:
            print("Server not running.")
            asyncio.loop.call_soon(asyncio.run(start_server()))
            print("Server restarted.")
    time.sleep(60)
"""


async def server_update():
    while git_checkout():
        asyncio.cancel(start_server())
        asyncio.run(start_server())



asyncio.ensure_future(git_checkout_loop())
asyncio.ensure_future(start_server())
asyncio.ensure_future(server_update())
event_loop = asyncio.get_event_loop()
asyncio.set_event_loop(event_loop)
event_loop.run_forever()
