import json

# File paths
USER_FILE = "users.json"
QUIZ_FILE = "quiz_data.json"
SCORES_FILE = "scores.json"

# Load data from JSON files
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Save data to JSON files
def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# User Registration
def register(users):
    print("\n--- Register ---")
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists. Try logging in.")
        return users
    password = input("Enter a password: ")
    users[username] = password
    save_data(USER_FILE, users)
    print("Registration successful!")
    return users

# User Login
def login(users):
    print("\n--- Login ---")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid username or password.")
        return None

# Quiz Function
def start_quiz(quiz_data, scores, username):
    print("\nChoose a quiz section:")
    sections = list(quiz_data.keys())
    for i, section in enumerate(sections, 1):
        print(f"{i}. {section}")
    choice = input("Enter the number of your choice: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(sections):
        print("Invalid choice!")
        return
    section = sections[int(choice) - 1]
    print(f"\n--- {section} Quiz ---")
    score = 0
    for i, question_data in enumerate(quiz_data[section], 1):
        print(f"\nQ{i}. {question_data['question']}")
        for j, option in enumerate(question_data['options'], 1):
            print(f"{j}. {option}")
        answer = input("Enter the number of your answer: ")
        if answer == question_data["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was {question_data['answer']}.")
    print(f"\nYou scored: {score}/{len(quiz_data[section])}")
    # Update scores
    if username not in scores:
        scores[username] = {}
    scores[username][section] = score
    save_data(SCORES_FILE, scores)

# Main Function
def main():
    users = load_data(USER_FILE)
    quiz_data = load_data(QUIZ_FILE)
    scores = load_data(SCORES_FILE)
    print("Welcome to the Quiz App!")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            users = register(users)
        elif choice == "2":
            username = login(users)
            if username:
                while True:
                    print("\n1. Start Quiz\n2. View Scores\n3. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        start_quiz(quiz_data, scores, username)
                    elif user_choice == "2":
                        user_scores = scores.get(username, {})
                        print(f"\n--- Scores for {username} ---")
                        for section, score in user_scores.items():
                            print(f"{section}: {score}")
                    elif user_choice == "3":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Try again.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
