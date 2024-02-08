import requests
from distutils.version import StrictVersion


def check_update(package_name, current_version):
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        latest_version = data["info"]["version"]
        if StrictVersion(current_version) < StrictVersion(latest_version):
            print(f"A new version of {package_name} is available: {latest_version}")
        else:
            print(f"You are using the latest version ({current_version}) of {package_name}.")
    except requests.exceptions.RequestException as e:
        print("Failed to check for updates:", str(e))
    except KeyError:
        print("Failed to parse response data.")
    except Exception as e:
        print("An error occurred:", str(e))
