FZF_FILE_SELECTOR_DIR="${FZF_FILE_SELECTOR_DIR-${0:A:h}}"
PYTHON="${FZF_FILE_SELECTOR_PYTHON:-python}"

function _fzf_file_selector() {
    read cursor buffer <<< $("${PYTHON}" "${FZF_FILE_SELECTOR_DIR}/fzf_file_selector.py" "${BUFFER}" "${CURSOR}")
    if [[ "$cursor" != "" ]] then
        BUFFER="${buffer}"
        CURSOR="${cursor}"
    fi
}
