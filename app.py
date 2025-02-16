import sqlite3

from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML-шаблон для ввода названия фильма
HTML_TEMPLATE = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Movie Input</title>
</head>
<body style="background-color: #CDB89D; text-align: center; font-family: Arial, sans-serif; color: #422F28;">

    <h1 style="color: #5E2611;">Введите название фильма</h1>
    <form method="POST" style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); width: 60%;">
        <input type="text" name="movieName" required 
               style="width: 100%; padding: 15px; font-size: 18px; border: 2px solid #6A6F4C; border-radius: 8px;">
        <br><br>
        <input type="submit" value="Отправить" 
               style="background-color: #5E2611; color: #FFFFFF; font-size: 18px; padding: 12px 24px; border: 3px solid #422F28; border-radius: 8px; cursor: pointer;">
    </form>
    <a href="/list" 
   style="position: absolute; top: 20px; left: 20px; background-color: #5E2611; color: #FFFFFF; font-size: 18px; 
          padding: 12px 24px; border: 3px solid #422F28; border-radius: 8px; cursor: pointer; text-decoration: none;">
    Фильмы
</a>

</body>
</html>
"""

htmlTemplateWithoutError = (
    HTML_TEMPLATE
    + """<h2 style="color: #6A6F4C; margin-top: 20px;">Фильм успешно добавлен</h2>
"""
)
html_with_error = (
    HTML_TEMPLATE
    + """<h2 style="color: #5E2611; margin-top: 20px;">Этот фильм уже присутствует в базе данных</h2>
"""
)

htmlMoviesList = """<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Список фильмов</title>
</head>
<body style="background-color: #CDB89D; text-align: center; font-family: Arial, sans-serif; color: #422F28; padding: 20px;">

    <h1 style="color: #5E2611;">Фильмы:</h1>

    <div style="background-color: #6A6F4C; color: #FFFFFF; padding: 20px; border-radius: 12px; max-width: 60%; margin: 0 auto; font-size: 18px; line-height: 1.6;">
    
"""
BACK_BUTTON = """</div>
            <a href="/" 
   style="position: absolute; top: 20px; left: 20px; background-color: #5E2611; color: #FFFFFF; font-size: 18px; 
          padding: 12px 24px; border: 3px solid #422F28; border-radius: 8px; cursor: pointer; text-decoration: none;">
    Назад
</a>

</body>
</html>"""


def delete_movie(movie_name):
    try:
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM movies WHERE movieName = ?", (movie_name,))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка удаления фильма: {e}")


def getMovies() -> list:
    try:
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT `movieName` from `movies`")
            movies = [row[0] for row in cursor.fetchall()]
            return movies
    except Exception:
        return None


def save_movie(movie_name):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `movies` (movieName) VALUES (?)", (movie_name,))
    conn.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        movie_name = request.form["movieName"]
        try:
            save_movie(movie_name)
            return render_template_string(htmlTemplateWithoutError)
        except sqlite3.IntegrityError:
            return html_with_error
    return render_template_string(HTML_TEMPLATE)


@app.route("/list", methods=["GET", "POST"])
def list():
    if request.method == "POST":
        movie_to_delete = request.form.get("movieName")
        if movie_to_delete:
            delete_movie(movie_to_delete)

    movies = getMovies()
    if movies is None:
        return "Ошибка при получении списка фильмов", 500

    # Генерация списка фильмов с кнопками удаления
    listOfMovies = "".join(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background-color: #5E2611;
                    color: #FFFFFF; padding: 10px; border-radius: 6px; margin: 10px auto; max-width: 50%;">
            <span style="font-size: 18px;">{movie}</span>
            <form method="POST" style="margin: 0;">
                <input type="hidden" name="movieName" value="{movie}">
                <button type="submit" style="background-color: #CDB89D; color: #5E2611; font-size: 16px; padding: 8px 16px; 
                                              border: 2px solid #422F28; border-radius: 6px; cursor: pointer;">
                    Удалить
                </button>
            </form>
        </div>
        """
        for movie in movies
    )

    BACK_BUTTON = """</div>
            <a href="/" 
   style="position: absolute; top: 20px; left: 20px; background-color: #5E2611; color: #FFFFFF; font-size: 18px; 
          padding: 12px 24px; border: 3px solid #422F28; border-radius: 8px; cursor: pointer; text-decoration: none;">
    Назад
</a>

</body>
</html>"""

    return render_template_string(htmlMoviesList + listOfMovies + BACK_BUTTON)


if __name__ == "__main__":
    app.run(debug=True)
