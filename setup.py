from cx_Freeze import setup, Executable

setup(
    name='Pinger',
    options={
        'build_exe': {
            'packages': ['configparser', 'hashlib', 'PySimpleGUI', 'platform', 'subprocess', 're', 'ping', 'time'],
            'include_files': [('settings.ini', 'data/settings.ini'), ('translation.ini', 'data/translation.ini')],
        },
    },
    version='1.0.0',
    description='This is simple software what **ping** all provided ip addresses or hostnames.',
    executables=[Executable('pinger.py')]
)
