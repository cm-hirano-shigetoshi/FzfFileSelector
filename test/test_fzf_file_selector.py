import fzf_file_selector
import pytest


@pytest.mark.parametrize(
    "d,home,expected",
    [
        ("/Users/sample.user/aaa", "/Users/sample.user", "~/aaa/"),
        ("/absolute/path", "/Users/sample.user", "/absolute/path/"),
    ],
)
def test_get_absdir_view(d, home, expected):
    response = fzf_file_selector.get_absdir_view(d, home_dir=home)
    assert response == expected


@pytest.mark.parametrize("d,expected", [(".", ".."), ("/Users", "/"), ("/", "/")])
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


@pytest.mark.parametrize(
    "d,path_type,type_,expected",
    [
        (".", "relative", "f", "fd --type f --color always ^ ."),
        (".", "absolute", "f", "fd --absolute-path --type f --color always ^ ."),
        (".", "absolute", "A", "fd --absolute-path --color always ^ ."),
        (".", "relative", "A", "fd --color always ^ ."),
    ],
)
def test_get_fd_command(d, path_type, type_, expected):
    response = fzf_file_selector.get_fd_command(d, path_type, type_)
    assert response == expected


@pytest.mark.parametrize(
    "key,value,expected",
    [
        (
            "key",
            None,
            "--key",
        ),
        (
            "key",
            123,
            "--key '123'",
        ),
        (
            "key",
            ["abc", "def"],
            "--key 'abc' --key 'def'",
        ),
    ],
)
def test_option_to_shell_string(key, value, expected):
    response = fzf_file_selector.option_to_shell_string(key, value)
    assert response == expected


@pytest.mark.parametrize(
    "abs_dir,expected",
    [
        (
            "/absolute/path/",
            "--reverse --header '/absolute/path/'",
        ),
        (
            "/",
            "--reverse --header '/'",
        ),
    ],
)
def test_get_fzf_options_view(abs_dir, expected):
    response = fzf_file_selector.get_fzf_options_view(abs_dir)
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
