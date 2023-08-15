import fzf_file_selector


def test_get_abspath():
    path = "/Users/sample.user/aaa"
    expected = "~/aaa"
    response = fzf_file_selector.get_abspath(path, home_dir="/Users/sample.user")
    assert response == expected


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


def test_get_origin_path_query_01():
    b = "aaa/bbbccc"
    c = 7
    expected = ("aaa", "bbb")
    response = fzf_file_selector.get_origin_path_query(b, c)
    assert response == expected


def test_get_origin_path_query_02():
    b = "ls aaa/bbbccc"
    c = 10
    expected = ("aaa", "bbb")
    response = fzf_file_selector.get_origin_path_query(b, c)
    assert response == expected


def test_get_fd_command():
    d = "."
    expected = "fd --type f --color always ^ ."
    response = fzf_file_selector.get_fd_command(d)
    assert response == expected


def test_get_fzf_options():
    d = "."
    query = "aaa"
    abs_path = "/ABSOLUTE"
    expected = "--listen 6266 --multi --ansi --reverse --header '/ABSOLUTE/' --query 'aaa' --bind 'alt-u:execute-silent(curl \"http://localhost:6366?origin_move=up\")' --bind 'alt-d:reload(fd --type d --color always ^ .)' --bind 'alt-f:reload(fd --type f --color always ^ .)' --bind 'alt-a:reload(fd --color always ^ .)'"
    response = fzf_file_selector.get_fzf_options(d, query, abs_path=abs_path)
    assert response == expected


def test_get_left_01():
    b = "aaabbb"
    c = 3
    expected = ""
    response = fzf_file_selector.get_left(b, c)
    assert response == expected


def test_get_left_02():
    b = "aaa bbb"
    c = 3
    expected = ""
    response = fzf_file_selector.get_left(b, c)
    assert response == expected


def test_get_left_03():
    b = "aaa bbb"
    c = 4
    expected = "aaa "
    response = fzf_file_selector.get_left(b, c)
    assert response == expected


def test_get_left_04():
    b = "aaa/bbbccc"
    c = 7
    expected = ""
    response = fzf_file_selector.get_left(b, c)
    assert response == expected


def test_get_right_01():
    b = "aaabbb"
    c = 3
    expected = "bbb"
    response = fzf_file_selector.get_right(b, c)
    assert response == expected


def test_get_right_02():
    b = "aaa bbb"
    c = 3
    expected = " bbb"
    response = fzf_file_selector.get_right(b, c)
    assert response == expected


def test_get_right_03():
    b = "aaa bbb"
    c = 4
    expected = "bbb"
    response = fzf_file_selector.get_right(b, c)
    assert response == expected


def test_get_right_04():
    b = "aaa/bbbccc"
    c = 7
    expected = "ccc"
    response = fzf_file_selector.get_right(b, c)
    assert response == expected


def test_get_buffer_from_items_01():
    b = "aaabbb"
    c = 3
    items = "select1\nselect2\n"
    expected = "select1 select2 bbb"
    response = fzf_file_selector.get_buffer_from_items(b, c, items)
    assert response == expected


def test_get_buffer_from_items_02():
    b = "ls test/abbb"
    c = 9
    items = "select1\nselect2\n"
    expected = "ls select1 select2 bbb"
    response = fzf_file_selector.get_buffer_from_items(b, c, items)
    assert response == expected


def test_get_cursor_from_items_01():
    b = "aaabbb"
    c = 3
    items = "select1\nselect2\n"
    expected = 16
    response = fzf_file_selector.get_cursor_from_items(b, c, items)
    assert response == expected


def test_get_cursor_from_items_02():
    b = "ls test/abbb"
    c = 9
    items = "select1\nselect2\n"
    expected = 19
    response = fzf_file_selector.get_cursor_from_items(b, c, items)
    assert response == expected
