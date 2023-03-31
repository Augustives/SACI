import os

from scraper.session.http_session import HttpSession
from scraper.session.response import Response
from scraper.session.utils import Methods
from scraper.websites.geeks_for_geeks.settings import LOGIN_URL


def get_login_payload():
    return {
        "reqType": "Login",
        "user": os.getenv("USERNAME"),
        "pass": os.getenv("PASSWORD"),
        "rem": False,
        "to": "https://auth.geeksforgeeks.org/?to=https://www.geeksforgeeks.org/",
        "rem": "on",
        "g-recaptcha-response": None,
        "browserInfo": {},
    }


async def follow_login(session: HttpSession):
    await session.request(
        method=Methods.GET.value,
        data=get_login_payload(),
        url=LOGIN_URL,
    )
