"""
Azure Login via MSAL.

requires the following environment variables:
AZURE_TENANT_ID
AZURE_REDIRECT_URI
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
"""

import json
import os

import streamlit as st
from msal import ConfidentialClientApplication
from streamlit.logger import get_logger

logger = get_logger("app")
logger.info("Start")

SCOPE = "User.Read"
AZURE_TENANT_ID = os.environ["AZURE_TENANT_ID"]
REDIRECT_URL = os.environ["AZURE_REDIRECT_URI"]

# var 1 is deprecated
# var 2 needs forwarding of auth_code_flow after redirect
#  only working solution so far is via cookie, that results in app reload problem:
#   https://github.com/NathanChen198/streamlit-cookies-controller/issues/10
#  alternative would be to store in a dict as cache_resource, using IP as key
#   but streamlit does not provide a way to get the IP:
#   https://github.com/streamlit/streamlit/issues/602
# hence my post at https://discuss.streamlit.io/t/msal-authentification-using-initiate-auth-code-flow-and-acquire-token-by-auth-code-flow/87911
MSAL_VAR = 1

if MSAL_VAR == 2:  # noqa: PLR2004
    # pip install streamlit-cookies-controller
    # this triggers app reload:
    #  https://github.com/NathanChen198/streamlit-cookies-controller/issues/10
    from streamlit_cookies_controller import CookieController

    cc = CookieController()


def login() -> None:
    """Display login link or handles redirect if already clicked."""
    app = initialize_app()
    code = st.query_params.get("code")
    if not code:
        st.header("Login")
        display_login_link(app=app)
        # st.stop()
    else:
        handle_redirect(app=app, code=code)
        # st.rerun()


def initialize_app() -> ConfidentialClientApplication:
    """Initialize the Azure app using Streamlit secrets.toml ."""
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]
    authority_url = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    return ConfidentialClientApplication(
        client_id=client_id, authority=authority_url, client_credential=client_secret
    )


def display_login_link(app: ConfidentialClientApplication) -> None:
    """Display the login at Azure link."""
    if MSAL_VAR == 1:  # deprecated:
        auth_url = app.get_authorization_request_url([SCOPE], redirect_uri=REDIRECT_URL)
    else:  # MSAL_VAR == 2: new:
        auth_code_flow = app.initiate_auth_code_flow(
            scopes=[SCOPE], redirect_uri=REDIRECT_URL
        )
        st.write("auth_code_flow", auth_code_flow)
        # {"state":"XXX","redirect_uri":"XXX","scope":["profile","offline_access","User.Read","openid"],"auth_uri":"XXX","code_verifier":"XXX","nonce":"XXX","claims_challenge":null} # noqa: E501
        auth_url = auth_code_flow["auth_uri"]
        # this now needs to be transferred to be reused after the redirect
        # st.session_state is not possible as the redirect results in a new session
        # trying to use cookie instead
        cc.set("auth_code_flow", auth_code_flow, max_age=600)  # 10 minutes

    st.write(
        f"<a href='{auth_url}' target='_self'>Click to Login</a>",
        unsafe_allow_html=True,
    )
    # https://login.microsoftonline.com/XXX/oauth2/v2.0/authorize?client_id=XXX&response_type=code&redirect_uri=XXX&scope=User.Read+offline_access+openid+profile


def handle_redirect(app: ConfidentialClientApplication, code: str) -> None:
    """
    Handle the redirect from Azure.

    sets st.session_state["USERNAME"]
    """
    logger.info("Performing login")
    username = get_username_from_azure(app, code)
    if username:
        st.session_state["USERNAME"] = username
        # remove auth data from url parameters
        d = st.query_params.to_dict()
        for param in ("code", "client_info", "session_state", "state"):
            if param in d:
                del d[param]
        st.query_params.from_dict(d)
    else:
        st.error("Login failed")
        st.stop()


def get_username_from_azure(app: ConfidentialClientApplication, code: str) -> str:
    """Acquire token using authorization code and return the username."""
    if MSAL_VAR == 1:  # deprecated:
        token_result = app.acquire_token_by_authorization_code(
            code, scopes=[SCOPE], redirect_uri=REDIRECT_URL
        )
    else:  # if MSAL_VAR == 2: # new
        auth_code_flow = cc.get("auth_code_flow")
        if type(auth_code_flow) is str:
            auth_code_flow = json.loads(auth_code_flow)
        assert type(auth_code_flow) is dict, type(auth_code_flow)

        auth_response = st.query_params.to_dict()
        st.write("auth_response", auth_response)
        # code, client_info, state, session_state

        token_result = app.acquire_token_by_auth_code_flow(
            auth_code_flow=auth_code_flow,
            auth_response=auth_response,
            scopes=[SCOPE],
            # redirect_uri=REDIRECT_URL,
        )
    assert isinstance(token_result, dict), type(token_result)
    st.write("token_result", token_result)

    # cspell: disable-next-line
    # {"token_type":"Bearer","scope":"User.Read profile openid email","expires_in":3948,"ext_expires_in":3948,"access_token":"XXX","refresh_token":"XXX","id_token":"XXX","client_info":"XXX","id_token_claims":{"aud":"XXX","iss":"https://login.microsoftonline.com/XXX/v2.0","iat":000,"nbf":000,"exp":000,"name":"name","oid":"XXX","preferred_username":"XXX","rh":"XXX","roles":["XXX"],"sub":"XXX","tid":"XXX","uti":"XXX","ver":"2.0"},"token_source":"identity_provider"}  # noqa: E501

    username = token_result.get("id_token_claims", {}).get("preferred_username", "")
    # user@myDomain.com
    access_token = token_result.get("access_token", "")
    if username == "" or access_token == "":  # nosec
        msg = "Auth failed"
        logger.error(msg)
        st.error(msg)
        st.stop()

    if not username.endswith("@myDomain.com"):
        msg = f"Bad username: '{username}'"
        logger.error(msg)
        st.error(msg)
        st.stop()

    logger.info("Auth successful: %s", username)

    # optionally fetch more user info from MS Graph API
    user_info = fetch_more_user_info(access_token)
    st.write("user_info", user_info)

    # return username.lower()
    return username[:-13].lower()  # drop @myDomain.com


def fetch_more_user_info(access_token: str) -> dict:
    """
    Optionally: Fetch user info from MS Graph API.
    """
    import requests  # noqa: PLC0415

    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=5,
    )
    # givenName, surname, mail, ...
    return response.json()


if "USERNAME" not in st.session_state:
    login()

if "USERNAME" in st.session_state:
    st.write(f"Logged in as: {st.session_state['USERNAME']}")

logger.info("End")
