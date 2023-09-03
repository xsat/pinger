from PySimpleGUI import Window
from time import strftime


LAST_CHECK_TEXT_KEY: str = 'LAST_CHECK_TEXT'

DEFAULT_TIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'


def restore_elements(window: Window, element_keys: list[str], default_element_background_color: str) -> None:
    def get_last_check_text() -> str:
        return strftime(DEFAULT_TIME_FORMAT)

    for element_key in element_keys:
        window[element_key].update(background_color=default_element_background_color)

    last_check_text: str = get_last_check_text()
    window[LAST_CHECK_TEXT_KEY].update(value=last_check_text)
    window.refresh()
