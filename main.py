import json
import random
import threading

def load_questions_from_file(file_path="questions.json"):
    """Charge les questions depuis un fichier JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            questions = json.load(file)
            # Validation basique pour vérifier la structure
            if not isinstance(questions, dict) or not all(
                isinstance(value, list) for value in questions.values()
            ):
                raise ValueError("Le fichier JSON est mal structuré.")
            return questions
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {file_path} contient des erreurs JSON.")
        exit(1)
    except ValueError as e:
        print(f"Erreur : {e}")
        exit(1)

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

def ask_question_with_timer(question_data, time_limit=10):
    """Pose une question avec une limite de temps pour répondre."""
    print("\n" + question_data["question"])
    for i, option in enumerate(question_data["options"], start=1):
        print(f"{i}. {option}")

    # Variable pour stocker la réponse
    answer = [None]

    # Fonction pour gérer le timer
    def timeout():
        if answer[0] is None:
            print("\n⏳ Temps écoulé ! La question est considérée comme incorrecte.")

    # Définir un timer
    timer = threading.Timer(time_limit, timeout)
    timer.start()

    while answer[0] is None:
        try:
            choice = input(f"Votre réponse (1-{len(question_data['options'])}) : ")
            if choice.isdigit() and 1 <= int(choice) <= len(question_data["options"]):
                answer[0] = int(choice)
                break
            else:
                print(f"Veuillez entrer un nombre entre 1 et {len(question_data['options'])}.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Annuler le timer si une réponse est donnée à temps
    timer.cancel()

    if answer[0] is None:
        return False  # Considérer la réponse comme incorrecte si le temps est écoulé

    return question_data["options"][answer[0] - 1] == question_data["answer"]

def save_score(player_name, category, score, total):
    """Enregistre le score du joueur dans un fichier scores.txt."""
    with open("scores.txt", "a") as file:
        file.write(f"{player_name},{category},{score}/{total}\n")

def display_top_scores():
    """Affiche les meilleurs scores enregistrés."""
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
            scores = [line.strip().split(",") for line in scores]
            scores = sorted(scores, key=lambda x: int(x[2].split("/")[0]), reverse=True)
            
            print("\n🏆 Meilleurs scores :")
            for rank, score in enumerate(scores[:5], start=1):
                print(f"{rank}. {score[0]} - {score[1]} - {score[2]}")
    except FileNotFoundError:
        print("\nAucun score enregistré pour le moment.")

def main():
    """Exécute le jeu de quiz."""
    print("Bienvenue dans le quiz de culture générale !\n")
    player_name = input("Entrez votre nom : ").strip()

    # Charger les questions depuis un fichier JSON
    questions = load_questions_from_file()
    categories = list(questions.keys())

    # Choisir une catégorie
    selected_category = choose_category(categories)
    print(f"\nVous avez choisi la catégorie : {selected_category}\n")

    # Filtrer les questions
    selected_questions = questions[selected_category]
    random.shuffle(selected_questions)

    score = 0
    for question_data in selected_questions:
        if ask_question_with_timer(question_data):
            print("Bonne réponse !")
            score += 1
        else:
            print(f"Faux ! La bonne réponse était : {question_data['answer']}.")

    print(f"\nQuiz terminé ! Votre score final est : {score}/{len(selected_questions)}")

    # Sauvegarder le score
    save_score(player_name, selected_category, score, len(selected_questions))

    # Afficher les meilleurs scores
    display_top_scores()

if __name__ == "__main__":
    main()
