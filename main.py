import streamlit as st
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Create a table to store movies and tags if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT,
                tags TEXT
            )''')
conn.commit()

# Function to add movie and tags to the database
def add_movie(movie, tags):
    c.execute("INSERT INTO movies (movie_name, tags) VALUES (?, ?)", (movie, ','.join(tags)))
    conn.commit()

# Function to get movies by tag from the database
def get_movies_by_tag(tag):
    c.execute("SELECT movie_name FROM movies WHERE tags LIKE ?", ('%'+tag.lower()+'%',))
    movies_with_tag = [row[0] for row in c.fetchall()]
    return movies_with_tag

# Function to get all available tags from the database
def get_all_tags():
    c.execute("SELECT DISTINCT tags FROM movies")
    all_tags = [tag.strip() for row in c.fetchall() for tag in row[0].split(',')]
    return all_tags

# Function to get tags and corresponding movies from the database
def get_tags_with_movies():
    c.execute("SELECT tags, movie_name FROM movies")
    tags_with_movies = {}
    for row in c.fetchall():
        tags = row[0].lower().split(',')
        movie = row[1]
        for tag in tags:
            if tag.strip() not in tags_with_movies:
                tags_with_movies[tag.strip()] = [movie]
            else:
                tags_with_movies[tag.strip()].append(movie)
    return tags_with_movies

# Function to delete a movie from the database
def delete_movie(movie):
    c.execute("DELETE FROM movies WHERE movie_name=?", (movie,))
    conn.commit()

# Streamlit app
st.title('Movie Tagging App')

# Input form to add movies and tags
st.header('Add Movies and Tags')
movie_name = st.text_input('Enter Movie Name')
movie_tags = st.text_input('Enter Tags (separated by commas)')

if st.button('Add Movie'):
    tags_list = [tag.strip().lower() for tag in movie_tags.split(',')]
    add_movie(movie_name, tags_list)
    st.success(f'Movie "{movie_name}" added with Tags: {", ".join(tags_list)}')

# Query movies by tag
st.header('Query Movies by Tag')
query_tag = st.selectbox('Select Tag to Query Movies', [''] + get_all_tags())
if st.button('Search'):
    if query_tag:
        movies_with_query_tag = get_movies_by_tag(query_tag)
        if movies_with_query_tag:
            st.success(f'Movies with Tag "{query_tag}":')
            for movie in movies_with_query_tag:
                st.write(f"- {movie}")
        else:
            st.warning(f'No movies found with Tag "{query_tag}"')
    else:
        st.warning('Please select a tag.')

# Display all tags and their corresponding movies
if st.button('Show All Tags'):
    st.header('All Tags and Movies')
    tags_with_movies = get_tags_with_movies()
    if tags_with_movies:
        for tag, movies in tags_with_movies.items():
            st.write(f"**{tag}**: ")
            for movie in movies:
                st.write(f"- {movie}")
    else:
        st.warning('No tags found yet.')


# Display all movies and their tags
if st.button('Show All Movies'):
    st.header('All Movies and Tags')
    c.execute("SELECT movie_name, tags FROM movies")
    all_movies = c.fetchall()
    if all_movies:
        for movie, tags in all_movies:
            st.write(f"## {movie}")
            st.write(f"Tags: {tags}")
            if st.button(f"Delete {movie}"):
                delete_movie(movie)
                st.success(f'Movie "{movie}" deleted successfully.')
    else:
        st.warning('No movies added yet.')


# Close the SQLite connection
conn.close()
