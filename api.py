import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
base_url = "https://api.hevyapp.com/v1"

headers = {
    "api-key": f"{API_KEY}"
}


def make_request(url):
    full_url = f"{base_url}{url}"
    r = requests.get(
        full_url,
        headers=headers
    )

    # convert json to a python dictionary
    print(r)
    data = json.loads(r.text)
    return data


def get_all_exercises():
    page = 1
    all_exercises = []
    page_size = 100

    while True:
        # pageSize 100 because that is max allowed by the API
        url = f"/exercise_templates?page={page}&pageSize={page_size}"

        # make request and get data
        data = make_request(url)
        exercises = data["exercise_templates"]
        all_exercises.extend(exercises)

        # break if no more exercises to fetch
        if len(exercises) < page_size:
            break
        page += 1
    return all_exercises

def get_exercise_history(exercise_id):
    url = f"/exercise_history/{exercise_id}"
    data = make_request(url)
    return data["exercise_history"]

