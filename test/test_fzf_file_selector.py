import fzf_file_selector


def test_get_parent_dir_01():
    d = "."
    expected = ".."
    response = fzf_file_selector.get_parent_dir(d)
    assert response == expected


def test_get_parent_dir_02():
    d = "/Users"
    expected = "/"
    response = fzf_file_selector.get_parent_dir(d)
    assert response == expected


def test_get_fd_command():
    d = "."
    expected = "fd --color always ^ ."
    response = fzf_file_selector.get_fd_command(d)
    assert response == expected


def test_get_fzf_options():
    d = "."
    expected = "--listen 6266 --multi --ansi --reverse --prompt './' --bind 'alt-u:execute-silent(curl \"http://localhost:6366?origin_move=up\")'"
    response = fzf_file_selector.get_fzf_options(d)
    assert response == expected


def get_left():
    b = "aaa"
    c = 3
    expected = "aaa"
    response = fzf_file_selector.get_left(b, c)
    assert response == expected


def get_right():
    b = "aaa"
    c = 3
    expected = "bbb"
    response = fzf_file_selector.get_right(b, c)
    assert response == expected


def test_get_buffer_from_items():
    b = "aaabbb"
    c = 3
    items = "select1\nselect2"
    expected = "aaa select1 select2 bbb"
    response = fzf_file_selector.get_buffer_from_items(b, c, items)
    assert response == expected


def test_get_cursor_from_items():
    b = "aaabbb"
    c = 3
    items = "select1\nselect2"
    expected = 20
    response = fzf_file_selector.get_cursor_from_items(b, c, items)
    assert response == expected
