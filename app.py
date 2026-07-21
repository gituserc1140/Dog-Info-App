import streamlit as st
import requests

GITHUB_REPO_URL = "https://github.com/gituserc1140/Dog-Info-App"
GITHUB_SPONSOR_URL = "https://github.com/sponsors/gituserc1140"


def apply_custom_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFF8F0;
        }
        h1, h2, h3 {
            color: #7B4F2E;
        }
        .stButton > button {
            background-color: #C17F53;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #A6663E;
            color: white;
        }
        [data-testid="stSidebar"] {
            background-color: #F5E6D3;
        }
        hr {
            border-color: #D4A57A;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def fetch_all_breeds(api_key):
    url = "https://api.thedogapi.com/v1/breeds"
    headers = {"x-api-key": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        return None, "The request timed out while loading breeds. Please try again."
    except requests.exceptions.RequestException:
        return None, "A network error occurred while loading breeds. Please try again."

    if response.status_code == 200:
        breeds = sorted(response.json(), key=lambda breed: (breed.get("name") or "Unknown breed").lower())
        return breeds, None
    if response.status_code in (401, 403):
        return None, "The API key is invalid or does not have access. Please verify your key."
    if response.status_code == 429:
        return None, "Rate limit reached for this API key. Please wait before retrying and check your TheDogAPI plan limits."
    return None, f"Failed to fetch breeds: HTTP {response.status_code}"


def fetch_breed_image(api_key, breed_id):
    url = "https://api.thedogapi.com/v1/images/search"
    headers = {"x-api-key": api_key}
    params = {"breed_ids": breed_id, "limit": 1, "has_breeds": 1}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            images = response.json()
            if images:
                return images[0].get("url"), None
            return None, None
        return None, f"Breed image lookup returned HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return None, "Breed image lookup timed out."
    except requests.exceptions.RequestException as exc:
        return None, f"Breed image lookup failed: {exc}"


def main():
    st.set_page_config(page_title="Dog Info App", page_icon="🐶", layout="centered")
    apply_custom_styles()
    st.title("🐶 Dog Info App")
    st.caption("Explore dog photos and breed details using your own TheDogAPI key.")

    st.sidebar.header("Settings")
    api_key_input = st.sidebar.text_input(
        "Enter your API Key from TheDogAPI",
        type="password",
    )
    api_key = api_key_input.strip()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&style=for-the-badge)]({GITHUB_REPO_URL})")
    st.sidebar.markdown(f"[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-GitHub-EA4AAA?logo=githubsponsors&style=for-the-badge)]({GITHUB_SPONSOR_URL})")

    if not api_key:
        st.info("Enter your TheDogAPI key in the sidebar to begin.")
        st.stop()

    breeds, error_message = fetch_all_breeds(api_key)
    if error_message:
        st.error(error_message)
        st.stop()

    if not isinstance(breeds, list) or not breeds:
        st.warning("No breeds were returned. Please try again.")
        st.stop()

    selected_breed = st.selectbox(
        "Select a dog breed",
        breeds,
        format_func=lambda breed: breed.get("name", "Unknown breed"),
    )

    breed_name = selected_breed.get("name", "Unknown breed")
    image_url = selected_breed.get("image", {}).get("url")
    breed_id = selected_breed.get("id")
    if not image_url and breed_id:
        image_url, image_error = fetch_breed_image(api_key, breed_id)
        if image_error:
            st.warning(image_error)

    if image_url:
        st.image(image_url, caption=breed_name)
    else:
        st.info("No image is currently available for this breed.")

    st.subheader(breed_name)
    st.write(f"**Temperament:** {selected_breed.get('temperament', 'Not available')}")
    st.write(f"**Life span:** {selected_breed.get('life_span', 'Not available')}")
    st.write(f"**Bred for:** {selected_breed.get('bred_for', 'Not available')}")
    st.markdown("---")

if __name__ == "__main__":
    main()