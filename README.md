# Dog-Info-App

Streamlit app for exploring dog images and breed details from [TheDogAPI](https://thedogapi.com/).

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&style=for-the-badge)](https://github.com/gituserc1140/Dog-Info-App)
[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-GitHub-EA4AAA?logo=githubsponsors&style=for-the-badge)](https://github.com/sponsors/gituserc1140)

## What the app does

- Lets users enter their own TheDogAPI key directly in the Streamlit UI
- Fetches dog images and shows related breed information
- Handles invalid keys and rate limits with clear feedback

## How to use

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Open the app in your browser.
5. Enter your TheDogAPI key in the sidebar.
6. Choose how many dogs to fetch and click **Fetch Dog Info**.

## API key

Create an API key at [TheDogAPI](https://thedogapi.com/) and paste it into the app sidebar when prompted.
