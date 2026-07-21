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


def fetch_dog_images(api_key, image_count):
    url = "https://api.thedogapi.com/v1/images/search"
    headers = {
        "x-api-key": api_key
    }
    params = {"limit": image_count, "has_breeds": 1}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.exceptions.Timeout:
        return None, "The request timed out. Please try again."
    except requests.exceptions.RequestException:
        return None, "A network error occurred while fetching dog data. Please try again."

    if response.status_code == 200:
        return response.json(), None
    if response.status_code in (401, 403):
        return None, "The API key is invalid or does not have access. Please verify your key."
    if response.status_code == 429:
        return None, "Rate limit reached for this API key. Please wait before retrying and check your TheDogAPI plan limits."
    return None, f"Failed to fetch images: HTTP {response.status_code}"


def fetch_breed_by_id(api_key, breed_id):
    url = f"https://api.thedogapi.com/v1/breeds/{breed_id}"
    headers = {"x-api-key": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, f"Breed lookup returned HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return None, "Breed lookup timed out."
    except requests.exceptions.RequestException as exc:
        return None, f"Breed lookup failed: {exc}"


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
    image_count = st.sidebar.slider("Number of dog images", min_value=1, max_value=10, value=3)

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&style=for-the-badge)]({GITHUB_REPO_URL})")
    st.sidebar.markdown(f"[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-GitHub-EA4AAA?logo=githubsponsors&style=for-the-badge)]({GITHUB_SPONSOR_URL})")

    if not api_key:
        st.info("Enter your TheDogAPI key in the sidebar to begin.")
        st.stop()

    if st.button("Fetch Dog Info"):
        images, error_message = fetch_dog_images(api_key, image_count)
        if error_message:
            st.error(error_message)
            st.stop()

        if not isinstance(images, list) or not images:
            st.warning("No dog images were returned for this request. Please try again.")
            st.stop()

        for image in images:
            breeds = image.get("breeds", [])

            # Fallback: if breeds list is empty and a breed_ids field is present
            # (returned by some TheDogAPI responses), fetch breed info by ID.
            if not breeds:
                breed_ids = image.get("breed_ids") or []
                if breed_ids:
                    breed_info, lookup_error = fetch_breed_by_id(api_key, breed_ids[0])
                    if breed_info:
                        breeds = [breed_info]
                    elif lookup_error:
                        st.warning(f"Could not load breed details for one image: {lookup_error}")

            if breeds:
                breed = breeds[0]
                st.image(image["url"], caption=breed.get("name", "Dog image"))
                st.subheader(breed.get("name", "Unknown breed"))
                st.write(f"**Temperament:** {breed.get('temperament', 'Not available')}")
                st.write(f"**Life span:** {breed.get('life_span', 'Not available')}")
                st.write(f"**Bred for:** {breed.get('bred_for', 'Not available')}")
            else:
                st.image(image["url"])
                st.write("Breed details are not available for this image.")
            st.markdown("---")

if __name__ == "__main__":
    main()