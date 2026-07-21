import streamlit as st
import requests

def fetch_dog_images(api_key):
    url = "https://api.thedogapi.com/v1/images/search"
    headers = {
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch images: {response.status_code}")
        return None

def main():
    st.title("Dog Image Viewer")
    api_key = st.text_input("Enter your API Key from TheDogAPI", type="password")

    if api_key:
        if st.button("Fetch Dog Images"):
            images = fetch_dog_images(api_key)
            if images:
                for image in images:
                    st.image(image["url"], caption="Dog Image")

if __name__ == "__main__":
    main()