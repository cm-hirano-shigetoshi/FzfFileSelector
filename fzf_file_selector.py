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


def get_absdir_view(path, home_dir=os.environ["HOME"]):
    abs_dir = os.path.abspath(path)
    if abs_dir.startswith(home_dir):
        abs_dir = "~" + abs_dir[len(home_dir) :]
    if abs_dir != "/":
        abs_dir += "/"
    return abs_dir


def get_parent_dir(d):
    if d.startswith("/"):
        # absolute path
        return os.path.abspath(os.path.dirname(d))
    else:
        # relative path
        return os.path.relpath(f"{d}/..")


def start_server():
    server = ThreadedHTTPServer(daemon=True)
    atexit.register(server.stop)
    server.start()


def get_origin_path_query(b, c):
    left = get_left(b, c)
    path = b[len(left) : c]
    if (pos := path.rfind("/")) == -1:
        origin_path = "."
        query = path
    else:
        origin_path = path[:pos]
        query = path[pos + 1 :]
    return origin_path, query


def get_fd_command(d, type_="f"):
    if type_ == "A":
        return f"{FD} --color always ^ {d}"
    else:
        return f"{FD} --type {type_} --color always ^ {d}"


def option_to_shell_string(key, value):
    if value is None:
        return f"--{key}"
    elif isinstance(value, list):
        strs = []
        for v in value:
            assert "'" not in str(v), f"Invalid option was specified: {v}"
            strs.append(f"--{key} '{v}'")
        return " ".join(strs)
    else:
        assert "'" not in str(value), f"Invalid option was specified: {value}"
        return f"--{key} '{value}'"


def options_to_shell_string(options):
    return [option_to_shell_string(k, v) for k, v in options.items()]


def get_fzf_options_core(d, query):
    options = {
        "listen": FZFZ_PORT,
        "multi": None,
        "ansi": None,
        "query": query,
        "bind": [
            f'alt-u:execute-silent(curl "http://localhost:{SERVER_PORT}?origin_move=up")',
            f'alt-p:execute-silent(curl "http://localhost:{SERVER_PORT}?origin_move=back")',
            f'alt-d:execute-silent(curl "http://localhost:{SERVER_PORT}?type=d")',
            f'alt-f:execute-silent(curl "http://localhost:{SERVER_PORT}?type=f")',
            f'alt-a:execute-silent(curl "http://localhost:{SERVER_PORT}?type=A")',
        ],
    }
    return " ".join(options_to_shell_string(options))


def get_fzf_options_view(abs_dir):
    return f"--reverse --header '{abs_dir}'"


def get_fzf_options(d, query):
    abs_dir = get_absdir_view(d)
    return f"{get_fzf_options_core(d, query)} {get_fzf_options_view(abs_dir)}"


def get_fzf_command(d, query):
    return f"{FZF} {get_fzf_options(d, query)}"


def get_buffer_via_fzf(command):
    proc = subprocess.run(command, shell=True, stdout=PIPE, text=True)
    return proc.stdout


def get_left(b, c):
    if c == 0:
        return ""
    if b[c - 1] == " ":
        return b[:c]
    else:
        pos = b[:c].rfind(" ")
        if pos == -1:
            return ""
        else:
            return b[: pos + 1]


def get_right(b, c):
    return b[c:]


def get_concat_items(items):
    return " ".join(items.rstrip("\n").split("\n"))


def get_buffer_from_items(b, c, items):
    concat_items = get_concat_items(items)
    left = get_left(b, c)
    right = get_right(b, c)
    if left == "":
        return f"{concat_items} {right}"
    else:
        if left[-1] == " ":
            return f"{left}{concat_items} {right}"
        else:
            return f"{left} {concat_items} {right}"


def get_cursor_from_items(b, c, items):
    if (left := get_left(b, c)) == "":
        return len(get_concat_items(items)) + 1
    elif left[-1] == " ":
        return len(left) + len(get_concat_items(items)) + 1
    else:
        return len(left) + 1 + len(get_concat_items(items)) + 1


def get_buffer_cursor(d, b, c):
    origin_path, query = get_origin_path_query(b, c)
    command = f"{get_fd_command(origin_path)} | {get_fzf_command(origin_path, query)}"
    items = get_buffer_via_fzf(command)
    if len(items) == 0:
        return None, None
    return get_buffer_from_items(b, c, items), get_cursor_from_items(b, c, items)


def get_fzf_api_url():
    return f"http://localhost:{FZFZ_PORT}"


def update_search_origins(move):
    if move == "up":
        if os.path.abspath(search_origins[-1]) != "/":
            search_origins.append(get_parent_dir(search_origins[-1]))
            return True
    elif move == "back":
        if len(search_origins) > 1:
            search_origins.pop(-1)
            return True
    return False


def get_origin_move_command(d):
    return f"reload({get_fd_command(d)})+change-header({get_absdir_view(d)})"


def get_type_command(type_):
    return f"reload({get_fd_command(search_origins[-1], type_=type_)})"


def request_to_fzf(params):
    try:
        if "origin_move" in params:
            move = params["origin_move"][0]
            succeeded = update_search_origins(move)
            if succeeded:
                command = get_origin_move_command(search_origins[-1])
                requests.post(get_fzf_api_url(), data=command)
                return True
        elif "type" in params:
            type_ = params["type"][0]
            command = get_type_command(type_)
            requests.post(get_fzf_api_url(), data=command)
        return True
    except Exception as e:
        print(e, file=sys.stderr)
        return False


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)
        succeeded = request_to_fzf(params)
        if succeeded:
            self.send_response(200)
            self.end_headers()

    def log_message(self, format, *args):
        # supress any log messages
        return


class ThreadedHTTPServer(threading.Thread):
    def run(self):
        self.httpd = HTTPServer(("", SERVER_PORT), RequestHandler)
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()


def main(args):
    org_buffer, org_cursor = args[1], int(args[2])
    origin_path = "."
    search_origins.append(origin_path)
    start_server()
    buffer, cursor = get_buffer_cursor(origin_path, org_buffer, org_cursor)
    if cursor:
        print(f"{cursor} {buffer}")


if __name__ == "__main__":
    main(sys.argv)
