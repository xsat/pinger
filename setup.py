from cx_Freeze import setup, Executable
from sys import platform, path


base = 'Win32GUI' if platform == 'win32' else None

setup(
    name='Pinger',
    options={
        'build_exe': {
            'path': path + ['pinger'],
            'packages': ['colors', 'ping', 'create_window_and_element_keys',
                         'ping_elements', 'restore_elements', 'PySimpleGUI'],
            'include_files': [('pinger/data/icon.ico', 'data/icon.ico'),
                              ('pinger/data/data.ini', 'data/data.ini'),
                              ('pinger/data/translation.ini', 'data/translation.ini')],
        },
    },
    version='1.0.0',
    description='This is simple software what ping all provided ip addresses or hostnames.',
    executables=[Executable('pinger/__main__.py', target_name='pinger', base=base, icon='pinger/data/icon.ico',)]
)
