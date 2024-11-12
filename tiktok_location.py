import sys
import json
import requests
from bs4 import BeautifulSoup
import pycountry


def get_country_info(region_code):
    region_code = region_code.upper()
    country = pycountry.countries.get(alpha_2=region_code)
    if not country:
        return None, None
    country_name = country.name
    flag_offset = 127397
    flag = ''.join(chr(ord(char) + flag_offset) for char in region_code)
    return country_name, flag


def fetch_tiktok_data(username):
    url = f"https://www.tiktok.com/@{username}"
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    })

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
    if not script_tag:
        print("Error: Data not found.")
        return

    try:
        json_data = json.loads(script_tag.string)
        user_info_path = json_data["__DEFAULT_SCOPE__"]["webapp.user-detail"]
        if "userInfo" not in user_info_path:
            print("Error: User info not found.")
            return

        region = user_info_path["userInfo"]['user']['region']
        country_name, flag = get_country_info(region)
        print(country_name, flag)

    except json.JSONDecodeError:
        print("Error parsing JSON data.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <username>")
        sys.exit(1)

    user = sys.argv[1]
    fetch_tiktok_data(user)
