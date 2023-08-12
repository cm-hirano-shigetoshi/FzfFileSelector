import os
import subprocess
import sys
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


def get_left(b, c):
    return b[:c]


def get_right(b, c):
    return b[c:]


def get_concat_items(items):
    return " ".join(items.rstrip("\n").split("\n"))


def get_buffer_from_items(b, c, items):
    concat_items = get_concat_items(items)
    left = get_left(b, c)
    right = get_right(b, c)
    return f"{left} {concat_items} {right}"


def get_cursor_from_items(b, c, items):
    return len(get_left(b, c)) + 1 + len(get_concat_items(items)) + 1


def get_buffer_cursor(b, c):
    command = f"{get_fd_command()} | {get_fzf_command()}"
    items = get_buffer_via_fzf(command)
    return get_buffer_from_items(b, c, items), get_cursor_from_items(b, c, items)


def main(args):
    org_buffer, org_cursor = args[1], int(args[2])
    buffer, cursor = get_buffer_cursor(org_buffer, org_cursor)
    print(f"{cursor} {buffer}")


if __name__ == "__main__":
    main(sys.argv)
