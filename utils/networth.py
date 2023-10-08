import requests
import json

def get_profiles(uuid):
    try:
        # Initialize variables
        best_networth = 0
        profile_ids = []
        profiles = {"stats": {"best_networth": "0"}, "profiles": {}}

        url = f"https://soopy.dev/api/v2/player_skyblock/{uuid}?networth=true"

        # api http request
        r = requests.get(url)

        # fetch profile ids from request data
        player_data = r.json()

        profiles_dict = player_data["data"]["profiles"]
        profile_ids = list(profiles_dict.keys())

        # loop through each profile and check networth and gamemmode
        for profile_id in profile_ids:
            profile_info = {}

            # fetch gamemode if profile type isn't normal
            if "gamemode" in player_data["data"]["profiles"][profile_id]["stats"]:
                profile_info["gamemode"] = player_data["data"]["profiles"][profile_id]["stats"]["gamemode"].replace("island", "stranded")
            else:
                profile_info["gamemode"] = "normal"

            # fetch networth
            networth = player_data["data"]["profiles"][profile_id]["members"][uuid]["nwDetailed"]["unsoulboundNetworth"]
            unsoulbound_networth = player_data["data"]["profiles"][profile_id]["members"][uuid]["nwDetailed"]["unsoulboundNetworth"]

            if networth > best_networth:
                best_networth = networth

            # append information to all profiles dict
            profile_info["networth"] = format_number(networth)
            profile_info["unsoulbound_networth"] = format_number(unsoulbound_networth)

            profiles["profiles"][profile_id] = profile_info

        # update best networth
        profiles["stats"]["best_networth"] = format_number(best_networth)
        return profiles

    except requests.RequestException as e:
        print(f"HTTP request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"An error occurred while trying to get networth: {e}")

    # if profiles are not fetched, return None
    return None
        
def format_number(num):
    if num < 1000:
        return f'{num:.2f}'
    elif num < 1000000:
        return f'{num / 1000:.2f}k'
    elif num < 1000000000:
        return f'{num / 1000000:.2f}m'
    else:
        return f'{num / 1000000000:.2f}b'
