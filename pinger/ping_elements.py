from PySimpleGUI import Window
from pinger.colors import GREEN_COLOR, RED_COLOR
from pinger.ping import ping


def ping_elements(window: Window, element_keys: list[str]) -> None:
    def get_background_color(is_success_status: bool) -> str:
        if is_success_status:
            return GREEN_COLOR

        return RED_COLOR

    for element_key in element_keys:
        address: str = window[element_key].metadata
        is_ping_success: bool = ping(address)
        new_background_color: str = get_background_color(is_ping_success)
        window[element_key].update(background_color=new_background_color)
        window.refresh()
