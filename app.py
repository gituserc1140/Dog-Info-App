import streamlit as st
import requests

GITHUB_REPO_URL = "https://github.com/gituserc1140/Dog-Info-App"
GITHUB_SPONSOR_URL = "https://github.com/sponsors/gituserc1140"


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
        return None, "Rate limit reached for this API key. Please wait and try again."
    return None, f"Failed to fetch images: HTTP {response.status_code}"

def main():
    st.set_page_config(page_title="Dog Info App", page_icon="🐶", layout="centered")
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

        for image in images:
            breeds = image.get("breeds", [])
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