# Pinger

This is simple software what **ping** all provided ip addresses or hostnames.

## Setup

You modify `settings.ini` file for your needs, example:

```ini
[localhost test]
test localhost = localhost

[Router test]
test 192.168.1.1 = 192.168.1.1
test 192.168.1.2 = 192.168.1.2
test 192.168.1.124 = 192.168.1.124

[Google test]
test 8.8.8.8 = 8.8.8.8
test 8.8.4.4 = 8.8.4.4
```

Explanation for first group in `settings.ini`

- `[localhost test]` group title is **required**
- `test localhost` item title  is **required**
- `localhost` ip or hostname is **required**

## Build

You can build program using console command:

```shell
python setup.py build
```

### Example of just started program
![Just started program](/screenshots/just_started_program.jpg)

### Example of test finished program
![Test finished program](/screenshots/test_finished_program.jpg)