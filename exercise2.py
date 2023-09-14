import sqlite3

# Read the file and copy its content to a list
stephen_king_adaptations_list = []
with open("stephen_king_adaptations.txt", "r") as file:
    stephen_king_adaptations_list = file.readlines()

# Establish a connection to the SQLite database
conn = sqlite3.connect("stephen_king_adaptations.db")
cursor = conn.cursor()

# Create the table
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                    movieID INTEGER PRIMARY KEY AUTOINCREMENT,
                    movieName TEXT,
                    movieYear INTEGER,
                    imdbRating REAL
                )''')

# Insert data from the list into the table
for line in stephen_king_adaptations_list:
    movie_info = line.strip().split(",")
    cursor.execute("INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating) VALUES (?, ?, ?)",
                   (movie_info[0], int(movie_info[1]), float(movie_info[2])))

# Function to search for movies in the database
def search_movies(option):
    if option == 1:
        movie_name = input("Enter the name of the movie: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
    elif option == 2:
        movie_year = input("Enter the year: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (movie_year,))
    elif option == 3:
        rating_limit = float(input("Enter the minimum rating: "))
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating_limit,))
    return cursor.fetchall()

# User interaction loop
while True:
    print("Options:")
    print("1. Search by Movie name")
    print("2. Search by Movie year")
    print("3. Search by Movie rating")
    print("4. STOP")

    user_option = int(input("Enter your choice: "))
    if user_option == 4:
        break

    result = search_movies(user_option)

    if not result:
        print("No matching movies found in the database.")
    else:
        for row in result:
            print("Movie Name:", row[1])
            print("Movie Year:", row[2])
            print("IMDb Rating:", row[3])
    
# Commit changes and close the database connection
conn.commit()
conn.close()