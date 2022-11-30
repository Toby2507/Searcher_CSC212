import json
from tkinter import Button, Listbox, Text, Tk

import matplotlib.pyplot as plt
import numpy as np
import requests


class Searcher:
    def __init__(self, root: Tk):
        self.root = root
        self.setup_window()
        self.search_bar = self.setup_search_bar()
        self.list_box = self.setup_list_box()
        self.setup_search_button()
        self.setup_view_pie_chart_button()
        root.mainloop()

    def setup_list_box(self):
        listbox = Listbox(self.root)
        listbox.place(width=460, height=348, x=20, y=64)
        return listbox

    def setup_search_bar(self):
        searchbar = Text(self.root, borderwidth=1)
        searchbar.place(x=20, y=17, width=342, height=28)
        return searchbar

    def setup_window(self):
        self.root.geometry("500x500")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

    def setup_search_button(self):
        button = Button(self.root, text="Search", background="#D9D9D9",
                        borderwidth=1, command=lambda: self.search_movie())
        button.place(x=368, y=17, width=112, height=28)

    def setup_view_pie_chart_button(self):
        button = Button(self.root, text="VIEW PIE CHART", background="#D9D9D9",
                        borderwidth=1, command=lambda: self.show_pie_chart())
        button.place(x=145, y=424, width=209, height=60)

    def search_movie(self):
        movie_name = self.search_bar.get("1.0", "end-1c").replace(" ", "+")
        movies = Searcher.get_movies(movie_name)
        genres = Searcher.get_genres(movies)
        self.display_genres(genres)

    def display_genres(self, genres):
        text = "{genre} - {count}"
        for genre in genres.keys():
            self.list_box.insert("end", text.format(
                genre=genre, count=genres[genre]))
            self.list_box.insert("end", "")

    def show_pie_chart(self):
        movie_name = self.search_bar.get("1.0", "end-1c").replace(" ", "+")
        movies = Searcher.get_movies(movie_name)
        genres = Searcher.get_genres(movies)
        genre_names = genres.keys()
        genre_counts = np.array([genres[name] for name in genre_names])
        plt.pie(genre_counts, labels=genre_names)
        plt.show()

    @staticmethod
    def get_movies(name):
        res = requests.get(f"http://www.omdbapi.com/?apikey=2af385ca&s={name}")
        return json.loads(res.text)["Search"]

    @staticmethod
    def get_movie_genres(movie_id):
        res = requests.get(
            f"http://www.omdbapi.com/?apikey=2af385ca&i={movie_id}")
        obj = json.loads(res.text)
        genres = obj["Genre"].split(", ")
        return genres

    @staticmethod
    def get_genres(movies):
        movie_ids = [movie["imdbID"] for movie in movies]
        genres = {}
        for movie_id in movie_ids:
            movie_genres = Searcher.get_movie_genres(movie_id)
            for genre in movie_genres:
                if genre in genres:
                    genres[genre] += 1
                else:
                    genres[genre] = 1
        return genres


Searcher(Tk())
