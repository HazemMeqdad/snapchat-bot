import json
import requests
import typing as t
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}

def get_user_story(username: str) -> t.Optional[t.List[t.Any]]:
    """
    Get user story from snapchat.
    """
    S = f"https://story.snapchat.com/@{username}"
    x = requests.get(S, headers=headers)
    soup = BeautifulSoup(x.content, "html.parser")
    snaps = soup.find(id="__NEXT_DATA__").string.strip()
    data = json.loads(snaps)
    try:
        return data["props"]["pageProps"]["story"]["snapList"]
    except KeyError:
        return None

def get_user_data(username: str) -> t.Optional[t.Dict[str, t.Any]]:
    """
    Get user data from snapchat.
    """
    S = f"https://www.snapchat.com/add/{username}"
    x = requests.get(S, headers=headers)
    soup = BeautifulSoup(x.content, "html.parser")
    snaps = soup.find(id="__NEXT_DATA__").string.strip()
    data = json.loads(snaps)
    try:
        return data["props"]["pageProps"]["userProfile"]
    except KeyError:
        return None

