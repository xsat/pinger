from cx_Freeze import setup, Executable

base = None

executables = [Executable('main.py', base=base)]

packages = ['configparser', 'hashlib', 'PySimpleGUI', 'platform', 'subprocess', 're', 'ping', 'time', 'idna']
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name='Pinger',
    options=options,
    version='1.0.0',
    description='This is simple software what **ping** all provided ip addresses or hostnames.',
    executables=executables
)
