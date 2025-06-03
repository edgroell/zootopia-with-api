import json
import os


def load_data(file_path: str) -> list:
    """
    Loads data from json file.
    :param file_path: str indicating the path to the json file
    :return: all_data: list containing all data from the json file
    """
    with open(file_path, "r", encoding="utf-8") as handle:
        all_data = json.load(handle)

        return all_data


def get_skin_types(all_animals: list) -> list:
    """
    Collects all skin types available in the data set.
    :param all_animals: list containing all info on all animals.
    :return: skin_types: list containing all skin types.
    """
    skin_types = []

    for animal in all_animals:
        if animal.get("characteristics", {}).get("skin_type") not in skin_types:
            skin_types.append(animal.get("characteristics", {}).get("skin_type"))

    return skin_types


def get_user_choice_skin(skin_types: list) -> str:
    """
    Validates the skin choice given by the user.
    :param skin_types: list containing all skin types.
    :return: str containing the skin choice.
    """
    while True:
        user_choice_skin = input("\nEnter a skin type: ").lower().strip()
        if user_choice_skin in [skin_type.lower() for skin_type in skin_types]:

            return user_choice_skin

        print("Invalid skin type")


def extract_animals_selection(all_animals: list, user_choice_skin: str) -> list:
    """
    Extracts the animals selection from the user choice skin type.
    :param all_animals: list containing all info on all animals.
    :param user_choice_skin: str containing the skin choice.
    :return: selected_animals: list containing all selected animals.
    """
    selected_animals = []

    for animal in all_animals:
        if animal.get("characteristics", {}).get("skin_type").lower() == user_choice_skin:
            selected_animals.append(animal)

    return selected_animals


def get_select_skin(all_animals: list) -> list:
    """
    Displays and gets the skin type from the user.
    :param all_animals: list containing all info on all animals.
    :return: selected_animals: list containing all selected animals.
    """
    skin_types = get_skin_types(all_animals)

    print("\nHere are all the available skin types:")

    for skin_type in skin_types:
        print(f">>> {skin_type}")

    user_choice_skin = get_user_choice_skin(skin_types)
    selected_animals = extract_animals_selection(all_animals, user_choice_skin)

    return selected_animals


def get_user_choice_animals(all_animals: list):
    """
    Coordinates the entire selection of the user (i.e., all or some animals).
    :param all_animals: list containing all info on all animals.
    :return: all_animals or selected_animals: list containing all selected animals.
    """
    while True:
        user_choice = input("\nDo you want all animals or select by skin type? (all/skin): ").lower().strip()
        if user_choice == "all":

            return all_animals

        elif user_choice == "skin":

            return get_select_skin(all_animals)

        else:
            print("Please enter either 'all' or 'skin'.")


def serialize_animal(animal: dict) -> str:
    """
    Builds the entire string in html format for a given animal.
    :param animal: dict containing all data from given animal.
    :return: animals_cards: str containing all info of a given animal in html format.
    """
    animals_cards = ''

    locations = animal.get('locations', ['Location not found'])
    locations_string = ', '.join(locations)

    animals_cards += '<li class="cards__item">\n'
    animals_cards += ('<div class="card__title">'
                      + animal.get('name', 'Name not found')
                      + '</div>\n')
    animals_cards += '<div class="card__text">'
    animals_cards += '<ul>\n'
    animals_cards += ('<li>'
                      + '<strong>'
                      + 'Skin Type:'
                      + '</strong>'
                      + ' '
                      + animal.get('characteristics', {}).get('skin_type', 'Skin Type not found')
                      + '</li>\n')
    animals_cards += ('<li>'
                      + '<strong>'
                      + 'Diet:'
                      + '</strong>'
                      + ' '
                      + animal.get('characteristics', {}).get('diet', 'Diet not found')
                      + '</li>\n')

    if animal.get('characteristics', {}).get('type') is not None:
        animals_cards += ('<li>'
                          + '<strong>'
                          + 'Type:'
                          + '</strong>'
                          + ' '
                          + animal.get('characteristics', {}).get('type').capitalize()
                          + '</li>\n')

    animals_cards += ('<li>'
                      + '<strong>'
                      + 'Location(s):'
                      + '</strong>'
                      + ' '
                      + f"{locations_string}"
                      + '</li>\n')
    animals_cards += ('<li>'
                      + '<strong>'
                      + 'Lifespan:'
                      + '</strong>'
                      + ' '
                      + animal.get('characteristics', {}).get('lifespan', 'Lifespan not found')
                      + '</li>\n')

    if animal.get('characteristics', {}).get('top_speed') is not None:
        animals_cards += ('<li>'
                          + '<strong>'
                          + 'Top Speed:'
                          + '</strong>'
                          + ' '
                          + animal.get('characteristics', {}).get('top_speed')
                          + '</li>\n')

    animals_cards += '</ul>\n'
    animals_cards += '</div>\n'
    animals_cards += '</li>\n'

    return animals_cards


def get_animal_cards(selected_animals: list) -> str:
    """
    Builds the entire string in html format for all selected animals.
    :param selected_animals: list containing all info from selected animals.
    :return: animals_cards: str containing all info of all selected animals in html format.
    """
    animals_cards = ''

    for animal in selected_animals:
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


def inject_animal_cards(page_template: str, animal_cards: str) -> str:
    """
    Replaces the placeholder from the html template with data extracted from the json file (i.e., the animal cards).
    :param page_template: str containing all info from the html template file.
    :param animal_cards: str containing all info from all selected animals in html format.
    :return: final_page_content: str containing the final page in html format.
    """
    final_page_content = page_template.replace("__REPLACE_ANIMALS_INFO__", animal_cards)

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

    print(f"Page has been created at {file_path}")


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
        animals_data = load_data(os.path.join('data', 'animals_data.json'))
        selected_animals = get_user_choice_animals(animals_data)
        animals_cards = get_animal_cards(selected_animals)
        page_template = open_template(os.path.join('templates', 'animals_template.html'))
        final_page_content = inject_animal_cards(page_template, animals_cards)
        build_repository_page(final_page_content)

        if not get_user_choice_loop():
            break


if __name__ == "__main__":
    main()
