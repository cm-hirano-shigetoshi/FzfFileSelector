import fzf_file_selector
import pytest


def test_get_abspath():
    path = "/Users/sample.user/aaa"
    expected = "~/aaa"
    response = fzf_file_selector.get_abspath(path, home_dir="/Users/sample.user")
    assert response == expected


@pytest.mark.parametrize("d,expected", [(".", ".."), ("/Users", "/")])
def test_get_parent_dir(d, expected):
    response = fzf_file_selector.get_parent_dir(d)
    assert response == expected


@pytest.mark.parametrize(
    "b,c,expected",
    [("aaa/bbbccc", 7, ("aaa", "bbb")), ("ls aaa/bbbccc", 10, ("aaa", "bbb"))],
)
def test_get_origin_path_query(b, c, expected):
    response = fzf_file_selector.get_origin_path_query(b, c)
    assert response == expected


def test_get_fd_command():
    d = "."
    expected = "fd --type f --color always ^ ."
    response = fzf_file_selector.get_fd_command(d)
    assert response == expected


@pytest.mark.parametrize(
    "d,query,expected",
    [
        (
            ".",
            "aaa",
            "--listen 6266 --multi --ansi --query 'aaa' --bind 'alt-u:execute-silent(curl \"http://localhost:6366?origin_move=up\")' --bind 'alt-d:reload(fd --type d --color always ^ .)' --bind 'alt-f:reload(fd --type f --color always ^ .)' --bind 'alt-a:reload(fd --color always ^ .)'",
        ),
    ],
)
def test_get_fzf_options_core(d, query, expected):
    response = fzf_file_selector.get_fzf_options_core(d, query)
    assert response == expected


@pytest.mark.parametrize(
    "abspath,expected",
    [
        (
            "/absolute/path",
            "--reverse --header '/absolute/path/'",
        ),
    ],
)
def test_get_fzf_options_view(abspath, expected):
    response = fzf_file_selector.get_fzf_options_view(abspath)
    assert response == expected


@pytest.mark.parametrize(
    "b,c,expected",
    [
        ("aaabbb", 3, ""),
        ("aaa bbb", 3, ""),
        ("aaa bbb", 4, "aaa "),
        ("aaa/bbbccc", 7, ""),
    ],
)
def test_get_left(b, c, expected):
    response = fzf_file_selector.get_left(b, c)
    assert response == expected


@pytest.mark.parametrize(
    "b,c,expected",
    [
        ("aaabbb", 3, "bbb"),
        ("aaa bbb", 3, " bbb"),
        ("aaa bbb", 4, "bbb"),
        ("aaa/bbbccc", 7, "ccc"),
    ],
)
def test_get_right(b, c, expected):
    response = fzf_file_selector.get_right(b, c)
    assert response == expected


@pytest.mark.parametrize(
    "b,c,items,expected",
    [
        ("aaabbb", 3, "select1\nselect2\n", "select1 select2 bbb"),
        ("ls test/abbb", 9, "select1\nselect2\n", "ls select1 select2 bbb"),
    ],
)
def test_get_buffer_from_items(b, c, items, expected):
    response = fzf_file_selector.get_buffer_from_items(b, c, items)
    assert response == expected


@pytest.mark.parametrize(
    "b,c,items,expected",
    [
        ("aaabbb", 3, "select1\nselect2\n", 16),
        ("ls test/abbb", 9, "select1\nselect2\n", 19),
    ],
)
def test_get_cursor_from_items(b, c, items, expected):
    response = fzf_file_selector.get_cursor_from_items(b, c, items)
    assert response == expected
