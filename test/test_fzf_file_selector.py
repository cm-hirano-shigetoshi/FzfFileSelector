import fzf_file_selector


def test_get_fd_command():
    expected = "fd ^ ."
    response = fzf_file_selector.get_fd_command()
    assert response == expected


def test_get_fzf_command():
    expected = "fzf --multi"
    response = fzf_file_selector.get_fzf_command()
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
