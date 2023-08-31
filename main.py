from configparser import ConfigParser


SETTINGS_FILENAME: str = 'settings.ini'


def main() -> None:
    config: ConfigParser = ConfigParser()
    config.read(SETTINGS_FILENAME)

    for section_name in config.sections():
        for value_name in config[section_name]:
            print(value_name, config[section_name][value_name])


if __name__ == '__main__':
    main()
