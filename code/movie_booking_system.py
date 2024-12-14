import json
from datetime import datetime

# 1. General Utility Functions
def load_datasets():
    # Load user, movie, and showtime data from JSON files
    with open('data/users.json', 'r') as users_file:
        users = json.load(users_file)["users"]
    with open('data/movies.json', 'r') as movies_file:
        movies = json.load(movies_file)["movies"]
    with open('data/showtimes.json', 'r') as showtimes_file:
        showtimes = json.load(showtimes_file)["showtimes"]
    return users, movies, showtimes

def save_datasets(users, showtimes=None):
    # Save user data to a file; save showtimes if updated
    with open('data/users.json', 'w') as users_file:
        json.dump({"users": users}, users_file, indent=4)
    
    if showtimes:
        with open('data/showtimes.json', 'w') as showtimes_file:
            json.dump({"showtimes": showtimes}, showtimes_file, indent=4)

# List of valid movie genres
valid_genres = ("Sci-Fi", "Romance", "Fantasy", "Musical", "Documentary")

# 2. User Management Functions
def register_user(users, showtimes):
    # Register a new user with a unique username and preferred genre
    print("\n-- Register --")
    username = input("Enter a new username: ")
    while username in [user["username"] for user in users]:
        print("The username is not available, please try another one.")
        username = input("Enter a new username: ")

    password = input("Enter a new password: ") 
    name = input("Enter your first name: ")  
    surname = input("Enter your surname: ") 

    # Ask user to choose a genre from the valid list
    print(f"Select your preferred genre from: {', '.join(valid_genres)}")
    genre = input("Enter your preferred genre: ").strip()
    while genre not in valid_genres:
        print(f"Invalid genre. Please select from: {', '.join(valid_genres)}")
        genre = input("Enter your preferred genre: ").strip()

    # Generate user ID based on existing users
    if users:
        max_id = int(users[-1]["user_id"][1:])
        user_id = f"U{max_id + 1:04}"  # New ID is incremented from the last user ID
    else:
        user_id = "U0001"  # First user ID

    # Get the current registration date and time
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add new user details to the list
    users.append({
        "user_id": user_id,
        "name": name,
        "surname": surname,
        "username": username,
        "password": password,
        "preferred_genres": genre,
        "registration_date": registration_date,
        "booked_showtimes": []  # Empty list for bookings
    })

    save_datasets(users)  # Save updated user data
    print("Registration successful! Returning to the main menu...")

def login_user(users):
    # Allow user to log in by verifying credentials
    print("\n-- Login --")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful!")
            return user  # Return user data on successful login
    print("Incorrect username or password. Please try again.")
    return None  # Return nothing if login fails

def delete_account(users, user):
    # Confirm and delete the user's account
    confirm = input("Are you sure you want to delete your account? (y/n): ")
    if confirm.lower() == 'y':
        users.remove(user)  # Remove the user from the list
        print("Account successfully deleted!")
        return True
    print("Returning to the previous page.")
    return False

def view_user_info(user):
    # Show the user's personal details
    print("\n-- User Information --")
    print(f"Name: {user['name']} {user['surname']}")
    print(f"Username: {user['username']}")
    print(f"Preferred Genre: {user['preferred_genres']}")
    print(f"Registration Date: {user['registration_date']}")

# 3. Movie Management Functions
def search_movies(movies):
    # Find movies using a keyword in their title
    print("\n-- Search Movies --")
    keyword = input("Enter a keyword to search for movies: ").strip().lower()
    results = [movie for movie in movies if keyword in movie["Title"].lower()]

    if results:
        print(f"\nMovies matching the keyword '{keyword}':\n")
        for movie in results:
            rating_stars = '★' * int(movie['Rating'] // 2) + '☆' * (5 - int(movie['Rating'] // 2))
            print(f"Movie ID: {movie['Movie_id']} - {movie['Title']} - {movie['Genre']} (Rating: {rating_stars} {movie['Rating']})")
    else:
        print(f"No movies found containing the keyword '{keyword}'.")

def view_recommended_movies(user, movies):
    # Show movies based on user's preferred genre
    print("\n-- Recommended Movies --")
    recommendations = [movie for movie in movies if movie["Genre"] in user["preferred_genres"]]
    recommendations.sort(key=lambda x: x['Rating'], reverse=True)

    if recommendations:
        print(f"\nRecommended Movies for You:\n")
        for movie in recommendations:
            rating_stars = '★' * int(movie['Rating'] // 2) + '☆' * (5 - int(movie['Rating'] // 2))
            print(f"Movie ID: {movie['Movie_id']}")
            print(f"Title: {movie['Title']}")
            print(f"Genre: {movie['Genre']}")
            print(f"Rating: {rating_stars} ({movie['Rating']})")
            print(f"Director: {movie['Director']}")
            print('-' * 40)
    else:
        print("No recommendations available at the moment.")

def view_booking_history(user, showtimes, movies):
    # Show all movies the user has booked
    print("\n-- Booking History --")
    if not user["booked_showtimes"]:
        print("No bookings found.")
        return

    for booking_id in user["booked_showtimes"]:
        showtime = next((s for s in showtimes if s["showtime_id"] == booking_id), None)
        if showtime:
            movie_title = next((movie['Title'] for movie in movies if movie['Movie_id'] == showtime["movie_id"]), "Unknown Movie")
            print(f"Movie: {movie_title} - {showtime['cinema_name']} - {showtime['showtime']}")
        else:
            print(f"Booking ID {booking_id} not found.")

# 4. Showtime Management Functions
def view_showtimes_by_movie(showtimes, movies):
    # Show available showtimes for a specific movie
    print("\n-- View Showtimes by Movie --")
    movie_id = input("Enter the movie ID: ")

    if not any(showtime['movie_id'] == movie_id for showtime in showtimes):
        print("There is no showtime for selected movie.")
        return

    results = [showtime for showtime in showtimes if showtime["movie_id"] == movie_id and showtime["available_seats"] > 0]
    if results:
        movie_title = next((movie['Title'] for movie in movies if movie['Movie_id'] == movie_id), "Unknown Movie")
        print(f"Showtimes for Movie: {movie_title}:")
        results.sort(key=lambda x: datetime.strptime(x['showtime'], "%Y-%m-%d %H:%M"))
        for showtime in results:
            print(f"{showtime['showtime_id']} - {showtime['showtime']} (Seats Available: {showtime['available_seats']}) - {showtime['cinema_name']}")
    else:
        print("No available showtimes for the specified movie.")

def book_showtime(user, showtimes):
    # Book a seat for a user in a showtime
    print("\n-- Book a Showtime --")
    showtime_id = input("Enter the showtime ID: ")

    for showtime in showtimes:
        if showtime["showtime_id"] == showtime_id and showtime["available_seats"] > 0:
            showtime["available_seats"] -= 1  # Reduce available seats
            user["booked_showtimes"].append(showtime_id)  # Add booking to user's list
            print("Successfully booked a showtime!")
            return
    print("Unfortunately, the showtime is not available for booking.")

# Main Menu
def main():
    # Main program loop
    users, movies, showtimes = load_datasets()
    current_user = None

    while True:
        if not current_user:
            print("\n-- Homepage --")
            print("1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                current_user = login_user(users)
            elif choice == "2":
                register_user(users, showtimes)
            elif choice == "3":
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("\n-- User Dashboard --")
            print("1. Search Movies")
            print("2. View Recommended Movies")
            print("3. View Showtimes by Movie")
            print("4. Book a Showtime")
            print("5. View Booking History")
            print("6. View User Info")
            print("7. Delete Account")
            print("8. Logout")

            choice = input("Enter your choice: ")
            if choice == "1":
                search_movies(movies)
            elif choice == "2":
                view_recommended_movies(current_user, movies)
            elif choice == "3":
                view_showtimes_by_movie(showtimes, movies)
            elif choice == "4":
                book_showtime(current_user, showtimes)
                save_datasets(users, showtimes)
            elif choice == "5":
                view_booking_history(current_user, showtimes, movies)
            elif choice == "6":
                view_user_info(current_user)
            elif choice == "7":
                if delete_account(users, current_user):
                    save_datasets(users)
                    current_user = None
            elif choice == "8":
                print("Logged out successfully!")
                current_user = None
            else:
                print("Invalid choice. Please try again.")

# Start the program!
main()
