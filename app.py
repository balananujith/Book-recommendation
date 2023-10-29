import streamlit as st
import pandas as pd
import difflib
import pickle

df = pickle.load(open('Deployment/Book_list.pkl', 'rb'))
similarity = pickle.load(open('Deployment/similarity.pkl', 'rb'))

def get_recommended_books(book_name, df, similarity):
    list_of_titles = df['Title'].tolist()
    find_close_match = difflib.get_close_matches(book_name, list_of_titles)

    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_book = df[df['Title'] == close_match]['Index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_book]))
        sorted_list = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        recommended_books = []
        i = 1
        for book in sorted_list:
            index = book[0]
            title_from_index = df[df.index == index]['Title'].values[0]
            recommended_books.append(title_from_index)
            i += 1
            if i > 6:
                break

        return recommended_books
    else:
        return None

def get_recommended_genre(genre_name, df, similarity):
    list_of_genre = df['Genre'].tolist()
    find_close_match = difflib.get_close_matches(genre_name, list_of_genre)

    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_book = df[df['Genre'] == close_match]['Index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_book]))
        sorted_list = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        recommended_books = []
        i = 1
        for book in sorted_list:
            index = book[0]
            title_from_index = df[df.index == index]['Title'].values[0]
            recommended_books.append(title_from_index)
            i += 1
            if i > 10:
                break

        return recommended_books
    else:
        return None

    background-color: #ff5733; /* Change the color to your preference */
    color: white;
}
.button-primary:hover {
    background-color: #ff794d; /* Change the hover color to your preference */
}
</style>
"""

st.set_page_config(page_title="Book Recommendation System", page_icon=":books:", layout="wide", initial_sidebar_state="expanded")

# Inject the custom CSS into the app
st.markdown(button_css, unsafe_allow_html=True)

def main():
    list_of_genre = df['Genre'].unique().tolist()

    st.title("Book Recommendation System")

    genre_name = st.selectbox('Select your Genre:', list_of_genre)

    if st.button('Show Books', key="show_books", help="show_books", class_="button-primary"):

        recommended_genre = get_recommended_genre(genre_name, df, similarity)

        if recommended_genre:
            st.header('Recommended Books for you: ')
            for i, genre in enumerate(recommended_genre, start=1):
                st.write(f"{i}. {genre}")
        else:
            st.warning('No close matches found for the given book name.')

    book_name = st.text_input('Enter your Book name:')

    if st.button('Recommend', key="recommend", help="recommend", class_="button-primary"):
        recommended_books = get_recommended_books(book_name, df, similarity)

        if recommended_books:
            st.header('Recommended Books for you:')
            for i, book in enumerate(recommended_books, start=1):
                st.write(f"{i}. {book}")
        else:
            st.warning('No close matches found for the given book name.')

if __name__ == "__main__":
    main()
