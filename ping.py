from platform import system
from subprocess import check_output, CalledProcessError
from re import search, Match


WINDOWS_OS: str = 'Windows'
WINDOWS_PING_PARAM: str = '-n'
OTHER_PING_PARAM: str = '-c'

HOST_UNREACHABLE_PING_PATTERN: str = 'Destination host unreachable'
LOST_PACKAGE_PING_PATTERN: str = 'Lost = 1'


def is_matched(pattern: str, string: str) -> bool:
    search_result: Match[str] = search(pattern, string)

    return search_result is not None


def ping(hostname: str) -> bool:
    def get_ping_param() -> str:
        if system() == WINDOWS_OS:
            return WINDOWS_PING_PARAM

        return OTHER_PING_PARAM

    param: str = get_ping_param()
    command: list[str] = ['ping', param, '1', hostname]

    try:
        command_result: str = str(check_output(command))

        return (not is_matched(HOST_UNREACHABLE_PING_PATTERN, command_result)
                and not is_matched(LOST_PACKAGE_PING_PATTERN, command_result))
    except CalledProcessError:
        return False


if __name__ == '__main__':
    ping('localhost')
