from PySimpleGUI import theme, theme_element_background_color, WIN_CLOSED
from pinger.restore_elements import restore_elements
from pinger.ping_elements import ping_elements
from pinger.create_window_and_element_keys import create_window_and_element_keys, CLOSE_BUTTON_KEY, TEST_BUTTON_KEY


DEFAULT_THEME: str = 'Dark'


def pinger() -> None:
    theme(DEFAULT_THEME)

    window, element_keys = create_window_and_element_keys()
    default_element_background_color: str = theme_element_background_color()

    while True:
        event, _ = window.read()

        if event == WIN_CLOSED or event == CLOSE_BUTTON_KEY:
            break

        if event == TEST_BUTTON_KEY:
            restore_elements(window, element_keys, default_element_background_color)
            ping_elements(window, element_keys)

    window.close()


if __name__ == '__main__':
    pinger()
