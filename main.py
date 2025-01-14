import json
import random

def load_questions():
    """Charge les questions de quiz organisées par catégorie."""
    questions = {
        "Histoire": [
            {"question": "En quelle année a eu lieu le premier pas sur la Lune?", "options": ["1965", "1969", "1972", "1980"], "answer": "1969"},
            {"question": "Qui a peint La Joconde?", "options": ["Van Gogh", "Picasso", "Léonard de Vinci", "Rembrandt"], "answer": "Léonard de Vinci"}
        ],
        "Sciences": [
            {"question": "Quelle est la plus grande planète du système solaire?", "options": ["Mars", "Terre", "Jupiter", "Saturne"], "answer": "Jupiter"},
            {"question": "Combien de continents y a-t-il sur Terre?", "options": ["5", "6", "7", "8"], "answer": "7"}
        ],
        "Géographie": [
            {"question": "Quelle est la capitale de la France?", "options": ["Paris", "Londres", "Berlin", "Madrid"], "answer": "Paris"}
        ]
    }
    return questions

def choose_category(categories):
    """Affiche un menu pour choisir une catégorie et retourne la catégorie choisie."""
    print("\nChoisissez une catégorie :")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    while True:
        try:
            choice = int(input("Votre choix : "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            else:
                print(f"Veuillez entrer un nombre entre 1 et {len(categories)}.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def ask_question(question_data):
    """Pose une question et retourne si la réponse est correcte."""
    print("\n" + question_data["question"])
    for i, option in enumerate(question_data["options"], start=1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input("Votre réponse (1-4) : "))
            if 1 <= choice <= 4:
                break
            else:
                print("Veuillez entrer un nombre entre 1 et 4.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    return question_data["options"][choice - 1] == question_data["answer"]

def main():
    """Exécute le jeu de quiz."""
    print("Bienvenue dans le quiz de culture générale !\n")
    questions = load_questions()
    categories = list(questions.keys())

    # Choisir une catégorie
    selected_category = choose_category(categories)
    print(f"\nVous avez choisi la catégorie : {selected_category}\n")

    # Filtrer les questions
    selected_questions = questions[selected_category]
    random.shuffle(selected_questions)

    score = 0
    for question_data in selected_questions:
        if ask_question(question_data):
            print("Bonne réponse !")
            score += 1
        else:
            print(f"Faux ! La bonne réponse était : {question_data['answer']}.")

    print(f"\nQuiz terminé ! Votre score final est : {score}/{len(selected_questions)}")

if __name__ == "__main__":
    main()