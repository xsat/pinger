from configparser import ConfigParser
from platform import system
from subprocess import call, DEVNULL, STDOUT

SETTINGS_FILENAME: str = 'settings.ini'

WINDOWS_OS: str = 'Windows'
WINDOWS_PING_PARAM: str = '-n'
OTHER_PING_PARAM: str = '-c'


def main() -> None:
    config: ConfigParser = ConfigParser()
    config.read(SETTINGS_FILENAME)

    for section_name in config.sections():
        for value_name in config[section_name]:
            address = config[section_name][value_name]
            print(value_name, config[section_name][value_name], ping(address))


def ping(hostname: str) -> bool:
    if system() == WINDOWS_OS:
        param = WINDOWS_PING_PARAM
    else:
        param = OTHER_PING_PARAM

    command: list[str] = ['ping', param, '1', hostname]

    # todo: Process timeout cases
    return call(command, stdout=DEVNULL, stderr=STDOUT) == 0


if __name__ == '__main__':
    main()
