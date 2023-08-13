import atexit
import os
import subprocess
import sys
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import PIPE

import requests

FZF = os.environ.get("FZF_FILE_SELECTOR_FZF", "fzf")
FD = os.environ.get("FZF_FILE_SELECTOR_FD", "fd")

FZFZ_PORT = int(os.environ.get("FZF_FILE_SELECTOR_FZFZ_PORT", "6266"))
SERVER_PORT = int(os.environ.get("FZF_FILE_SELECTOR_SERVER_PORT", "6366"))

search_origins = []


def get_parent_dir(d):
    if d.startswith("/"):
        # absolute path
        return os.path.abspath(os.path.dirname(d))
    else:
        # relative path
        return os.path.relpath(f"{d}/..")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)

        if "origin_move" in params:
            if params["origin_move"][0] == "up":
                parent_dir = get_parent_dir(search_origins[-1])
                search_origins.append(parent_dir)

                requests.post(
                    f"http://localhost:{FZFZ_PORT}",
                    data=f"reload({get_fd_command(parent_dir)})+change-prompt({parent_dir}/)",
                )

                self.send_response(200)
                self.end_headers()
                self.wfile.write(parent_dir.encode())

    def log_message(self, format, *args):
        # supress any log messages
        return


class ThreadedHTTPServer(threading.Thread):
    def run(self):
        self.httpd = HTTPServer(("", SERVER_PORT), RequestHandler)
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()


def start_server():
    server = ThreadedHTTPServer(daemon=True)
    atexit.register(server.stop)
    server.start()


def get_fd_command(d):
    return f"{FD} --color always ^ {d}"


def get_fzf_options(d):
    return f"--listen {FZFZ_PORT} --multi --ansi --reverse --prompt '{d}/' --bind 'alt-u:execute-silent(curl \"http://localhost:{SERVER_PORT}?origin_move=up\")'"


def get_fzf_command(d):
    return f"{FZF} {get_fzf_options(d)}"


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


def get_buffer_cursor(d, b, c):
    command = f"{get_fd_command(d)} | {get_fzf_command(d)}"
    items = get_buffer_via_fzf(command)
    return get_buffer_from_items(b, c, items), get_cursor_from_items(b, c, items)


def main(args):
    org_buffer, org_cursor = args[1], int(args[2])
    origin_path = "."
    search_origins.append(origin_path)
    start_server()
    buffer, cursor = get_buffer_cursor(origin_path, org_buffer, org_cursor)
    print(f"{cursor} {buffer}")


if __name__ == "__main__":
    main(sys.argv)
