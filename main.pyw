import os
import sqlite3
import sys
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def getDataFromDatabase():
    data = []
    try:
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT `movieName` from movies")
            movieNames = cursor.fetchall()
            for row in movieNames:
                data.append(row[0])
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    return data


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("/src/clapperboard.ico"))
        self.movieList = QListWidget()
        self.movieList.itemClicked.connect(self.on_movie_selected)
        self.loadMovies()
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.restartButton = QPushButton("Перезапустить приложение")
        self.restartButton.clicked.connect(self.restart_application)
        self.checkbox = QCheckBox("Использовать kinopoisk")
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Введите название фильма")
        self.searchButton = QPushButton("Искать")
        self.searchButton.clicked.connect(self.search)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.inputField)
        layout.addWidget(self.searchButton)
        layout.addWidget(self.movieList)
        layout.addWidget(self.restartButton)
        central_widget.setLayout(layout)
        self.setWindowTitle("Поиск фильма")
        self.setGeometry(450, 300, 251, 520)
        self.setCentralWidget(central_widget)

    def restart_application(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def on_movie_selected(self, item):
        """Обрабатывает выбор фильма из списка."""
        selected_movie = item.text()
        self.inputField.setText(selected_movie)
        self.search()

    def loadMovies(self):
        movies = getDataFromDatabase()
        for movie in movies:
            self.movieList.addItem(movie.strip())

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш."""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.search()

    def search(self):
        query = self.inputField.text().strip()
        if not (self.checkbox.isChecked()) and query:
            # Формируем URL для поиска на Google с оператором inurl:
            search_query = " смотреть онлайн бесплатно inurl:lordfilm.md"
            search_url = f"https://www.google.com/search?q={query}   {search_query}"
        elif self.checkbox.isChecked() and query:
            base_url = "https://www.kinopoisk.ru/index.php?kp_query="
            search_url = base_url + query.replace(" ", "+")
        webbrowser.open(search_url)
        self.inputField.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("/src/clapperboard.ico"))
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
