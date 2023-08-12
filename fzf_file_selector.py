import os
import subprocess
from subprocess import PIPE

fzf = os.environ.get("FZF_FILE_SELECTOR_FZF", "fzf")
fd = os.environ.get("FZF_FILE_SELECTOR_FD", "fd")


def get_fd_command():
    return f"{fd} ^ ."


def get_fzf_command():
    return f"{fzf} --multi"


def get_buffer_via_fzf(command):
    proc = subprocess.run(command, shell=True, stdout=PIPE, text=True)
    return proc.stdout


def get_buffer_from_items(items):
    return " ".join(items.split("\n"))


def get_buffer():
    command = f"{get_fd_command()} | {get_fzf_command()}"
    items = get_buffer_via_fzf(command)
    return get_buffer_from_items(items)


def get_cursor(buffer):
    return len(buffer)


def main():
    buffer = get_buffer()
    cursor = get_cursor(buffer)
    print(f"{cursor} {buffer}")


if __name__ == "__main__":
    main()
