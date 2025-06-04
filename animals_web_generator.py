import requests
import os


API_KEY = 'U4eFBf4XnV+YdADZNn7EsA==q4NEVPb3NIUVrhoA'


def get_user_choice_animal() -> str:
    """
    Prompts user for an animal choice.
    :return: user_choice: str containing the animal choice.
    """
    while True:
        user_choice = input("\nEnter the name of an animal: ")
        if len(user_choice) > 0:

            return user_choice.strip()

        print("\nPlease enter a valid choice.")


def load_data(animal_name: str) -> list | str | None:
    """
    Loads data from Animals API (API Ninjas).
    :param animal_name: str indicating the name of the animal to be loaded.
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


def serialize_animal(animal: dict) -> str:
    """
    Builds the entire string in HTML format for a given animal.
    :param animal: dict containing all data from given animal.
    :return: str containing all info of a given animal in HTML format.
    """
    name = animal.get('name', 'Name not found')
    characteristics = animal.get('characteristics', {})
    locations = ', '.join(animal.get('locations', ['Location not found']))

    type_info = f"<li><strong>Type:</strong> {characteristics.get('type', '').capitalize()}</li>" \
        if characteristics.get('type') is not None else ''

    top_speed_info = f"<li><strong>Top Speed:</strong> {characteristics.get('top_speed')}</li>" \
        if characteristics.get('top_speed') is not None else ''

    animals_card = f"""
    <li class="cards__item">
        <div class="card__title">{name}</div>
        <div class="card__text">
            <ul>
                <li><strong>Skin Type:</strong> {characteristics.get('skin_type', 'Skin Type not found')}</li>
                <li><strong>Diet:</strong> {characteristics.get('diet', 'Diet not found')}</li>
                {type_info}
                <li><strong>Location(s):</strong> {locations}</li>
                <li><strong>Lifespan:</strong> {characteristics.get('lifespan', 'Lifespan not found')}</li>
                {top_speed_info}
            </ul>
        </div>
    </li>
    """
    return animals_card


def get_animal_cards(animals_data: list) -> str:
    """
    Builds the entire string in html format for all selected animals.
    :param animals_data: list containing all info from selected animals.
    :return: animals_cards: str containing all info of all selected animals in html format.
    """
    animals_cards = ''

    for animal in animals_data:
        animals_cards += serialize_animal(animal)

    return animals_cards


def open_template(file_path: str) -> str:
    """
    Reads the content of the html template file.
    :param file_path: str indicating the path to the html template file.
    :return: page_template: str containing all info from the html template file.
    """
    with open(file_path, "r", encoding="utf-8") as handle:
        page_template = handle.read()

        return page_template


def inject_website_content(page_template: str, website_content: str) -> str:
    """
    Replaces the placeholder from the html template with data extracted from the json file (i.e., the animal cards).
    :param page_template: str containing all info from the html template file.
    :param website_content: str containing all info from all selected animals in html format.
    :return: final_page_content: str containing the final page in html format.
    """
    final_page_content = page_template.replace("__REPLACE_ANIMALS_INFO__", website_content)

    return final_page_content


def build_repository_page(final_content: str) -> None:
    """
    Builds the final html page containing the animal cards.
    :param final_content: str containing the final page in html format.
    :return: None
    """
    if not os.path.exists('output'):
        os.mkdir('output')

    file_path = os.path.join('output', 'animals.html')

    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(final_content)

    print(f"Website was successfully generated at {file_path}")


def get_user_choice_loop() -> bool:
    """
    Prompts user whether to have another search or exit the program.
    :return: bool: handles user choice whether to continue or not.
    """
    while True:
        continue_or_exit = input("\nDo you want to continue? (y/n): ").lower().strip()
        if continue_or_exit == 'y':

            return True

        if continue_or_exit == 'n':
            print("\nGoodbye and see you next time!\n")

            return False

        print("Please enter 'y' or 'n'.")


def main():
    while True:
        animal_name = get_user_choice_animal()
        animals_data = load_data(animal_name)

        if not animals_data:
            if not get_user_choice_loop():
                break

        website_content = animals_data

        if type(animals_data) is list:
            animals_cards = get_animal_cards(animals_data)
            website_content = animals_cards

        page_template = open_template(os.path.join('templates', 'animals_template.html'))
        final_page_content = inject_website_content(page_template, website_content)
        build_repository_page(final_page_content)

        if not get_user_choice_loop():
            break


if __name__ == "__main__":
    main()
