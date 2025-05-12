from getpass import getpass
from os import getenv
from typing import Tuple

from tuya import TuyaAPI, InvalidAuthentication


def get_login() -> Tuple[str, str]:
    def ask_until_ok(fn) -> str:
        while True:
            try:
                return fn()
            except KeyboardInterrupt as e:
                print("Aborted.")
                raise
            except:
                pass
            print()
    return (
        getenv("LEDVANCE_USERNAME") or ask_until_ok(lambda: input("Please put your Tuya/Sylvania username: ")),
        getenv("LEDVANCE_PASSWORD") or ask_until_ok(lambda: getpass("Please put your Tuya/Sylvania password: "))
    )


def main():
    username, password = get_login()

    api = TuyaAPI(username, password)
    try:
        api.login()
    except InvalidAuthentication:
        print("Invalid authentication.")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")

    print('---------------------------')
    for group in api.groups():
        for dev in api.devices(group['groupId']):
            print(f'Device Name:\t{dev.name}')
            print(f'  Device ID:\t{dev.id}')
            print(f'  Local Key:\t{dev.localKey}')
            print('---------------------------')


if __name__ == "__main__":
    main()
