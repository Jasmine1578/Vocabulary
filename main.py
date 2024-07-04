from flask import Flask, render_template, url_for, request, redirect, session
from manager import connect_bd, create_tables, insert_values, all_vocab
import sqlite3

app= Flask(__name__)
bd_path = 'vocab.db'
create_tables(bd_path)
insert_values(bd_path)
app.secret_key = '78k'  # Секретный ключ для работы с сессиями
#word1 = 'aa'

# Функция для поиска слова в базе данных
def get_translation(word):
    word = word.strip().lower()
    #word1 = word
    #print(f"Looking up word: {word}")
    conn = sqlite3.connect('vocab.db')
    c = conn.cursor()
    c.execute("SELECT word_trans FROM vocab WHERE word_val = ?", (word,))
    result = c.fetchone()
    conn.close()
    if result:
        #print(f"Found definition: {result[0]}")
        return result[0]
    else:
        #print("No definition found")
        return None

''''@app.route("/")
def index():
    return render_template("index.html")'''
def add_word(word, translation):
    word = word.strip().lower()  # Удаляем пробелы и приводим к нижнему регистру
    translation = translation.strip().lower()
    print(f"Adding word: '{word}' with translation: '{translation}'")  # Логирование
    conn = sqlite3.connect('vocab.db')
    c = conn.cursor()
    c.execute("INSERT INTO vocab (word_val, word_trans) VALUES (?, ?)", (word, translation))
    conn.commit()
    conn.close()
    print("Word added successfully")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        word = request.form['word']
        session['word'] = word  # Сохраняем слово в сессии
        #print(f"Received word: {word}")
        translation = get_translation(word)
        if translation:
            #print(f"Translation to render: '{translation}'")
            return render_template('index1.html', translation = translation, error = None)
        else:
            #print("Rendering error message: 'Word not found.'")
            return render_template('index1.html', translation = None, error = "Слово не найдено в словаре.")
    return render_template('index1.html', translation = None, error = None)

    #return render_template("index1.html", vocab = all_vocab(bd_path))

@app.route('/add_word', methods=['POST'])
def add_word_route():
    #word = request.form['word']
    #word = request.args.get('word')
    word = session.get('word')  # Получаем слово из сессии
    if word is None:
        return "Error: Word parameter is missing."
    translation = request.form['translation']
    add_word(word, translation)
    session.pop('word', None)  # Удаляем слово из сессии после добавления
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True, port=8000)