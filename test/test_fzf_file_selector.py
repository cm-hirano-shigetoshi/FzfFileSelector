import fzf_file_selector


def test_get_fd_command():
    expected = "fd ^ ."
    response = fzf_file_selector.get_fd_command()
    assert response == expected


def test_get_fzf_command():
    expected = "fzf"
    response = fzf_file_selector.get_fzf_command()
    assert response == expected


def test_get_buffer_from_items():
    items = "aaa"
    expected = "aaa"
    response = fzf_file_selector.get_buffer_from_items(items)
    assert response == expected


def test_get_cursor():
    buffer = "aaa"
    expected = 3
    response = fzf_file_selector.get_cursor(buffer)
    assert response == expected
