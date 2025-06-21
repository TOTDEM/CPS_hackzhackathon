import requests
import json

# --- Configuration ---
# Base URL of your FastAPI server.
# Make sure this matches where your server is running (e.g., http://127.0.0.1:8000)
API_BASE_URL = "http://127.0.0.1:8000"

# --- Client Functions ---

def add_user(user_id: str):
    """
    Sends a POST request to add a new user to the server.
    :param user_id: The ID of the user to add.
    """
    url = f"{API_BASE_URL}/users/{user_id}/add"
    print(f"\n--- Adding user: {user_id} ---")
    try:
        response = requests.post(url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

def update_user_score(user_id: str, score_to_add: int):
    """
    Sends a POST request to update a user's score.
    :param user_id: The ID of the user whose score to update.
    :param score_to_add: The amount to add to the user's current score.
    """
    url = f"{API_BASE_URL}/users/{user_id}/score"
    payload = {"score": score_to_add}
    print(f"\n--- Updating score for {user_id} by {score_to_add} ---")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

def get_user_score(user_id: str):
    """
    Sends a GET request to retrieve a single user's score.
    :param user_id: The ID of the user whose score to retrieve.
    """
    url = f"{API_BASE_URL}/users/{user_id}/score"
    print(f"\n--- Getting score for user: {user_id} ---")
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

def get_all_users_scores():
    """
    Sends a GET request to retrieve scores for all users.
    """
    url = f"{API_BASE_URL}/users"
    print("\n--- Getting all users' scores ---")
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        print(f"Response content: {response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

# --- Example Usage ---
if __name__ == "__main__":
    # Ensure your FastAPI server is running before executing this script!
    # (e.g., uvicorn main:app --reload --port 8000)

    # 1. Add some users
    add_user("alice")
    add_user("bob")
    add_user("alice") # Try to add alice again to see the error handling
    add_user("charlie") # Add a new user
    

    # 2. Update scores
    update_user_score("alice", 100)
    update_user_score("bob", 50)
    update_user_score("alice", 25) # Add more to alice's score
    update_user_score("charlie", 75) # Add a new user directly by updating their score

    # 3. Get individual user scores
    get_user_score("alice")
    get_user_score("bob")
    get_user_score("charlie")
    get_user_score("diana") # Try to get a non-existent user to see error handling

    # 4. Get all users' scores
    get_all_users_scores()
