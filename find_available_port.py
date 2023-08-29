import sys
from http.server import HTTPServer


def run():
    httpd = HTTPServer(("", 0), None)
    return httpd.server_port


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_port = sys.argv[1]
        port = run(start_port=start_port)
    else:
        port = run()
    print(port, end="")
