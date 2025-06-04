import requests


def fetch_data(animal_name: str) -> list | str | None:
    """
    Fetches data from Animals API (API Ninjas) for the given animal.
    :param animal_name: str indicating the name of the animal to be fetched.
    :return:
        all_data: list containing all data from the API call
        no_data: str containing an error message signaling the animal doesn't seem to exist.
        None: if no data was loaded.
    """
    api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(animal_name)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    if response.status_code == requests.codes.ok:
        all_data = response.json()

        if all_data:

            return all_data

        if not all_data:
            no_data = "<h1>The animal '{}' doesn't exist - No data was loaded!</h1>".format(animal_name)

            return no_data

    print("Error:", response.status_code, response.text)

    return None