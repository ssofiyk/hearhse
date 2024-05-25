import sqlite3
import pandas as pd
from gtts import gTTS

df = pd.read_csv('table.csv')
con = sqlite3.connect("../db.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS words(id INTEGER PRIMARY KEY,"
            "text VARCHAR(255) NOT NULL,"
            "path VARCHAR(255) NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS phrases(id INTEGER PRIMARY KEY,"
            "text VARCHAR(255) NOT NULL,"
            "path VARCHAR(255) NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS sents(id INTEGER PRIMARY KEY,"
            "text VARCHAR(255) NOT NULL,"
            "path VARCHAR(255) NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS quests(id INTEGER PRIMARY KEY,"
            "text VARCHAR(255) NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS infs(id INTEGER PRIMARY KEY,"
            "text VARCHAR(255) NOT NULL,"
            "path VARCHAR(255) NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS miss_sents(id INTEGER PRIMARY KEY,"
            "text VARCHAR(255) NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY)")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_words(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, word_id INTEGER, score INTEGER, "
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id), "
    "FOREIGN KEY (word_id) REFERENCES words (id))")

cur.execute(
    "CREATE TABLE IF NOT EXISTS user_radio2words(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, word_id INTEGER, score INTEGER, "
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id), "
    "FOREIGN KEY (word_id) REFERENCES words (id))")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_radio4words(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, word_id INTEGER, score INTEGER, "
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id), "
    "FOREIGN KEY (word_id) REFERENCES words (id))")

cur.execute(
    "CREATE TABLE IF NOT EXISTS user_miss_sents(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, word_id INTEGER, score INTEGER, "
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id), "
    "FOREIGN KEY (word_id) REFERENCES words (id))")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_quest(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, word_id INTEGER, score INTEGER, "
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id), "
    "FOREIGN KEY (word_id) REFERENCES words (id))")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_inf(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, word_id INTEGER, score INTEGER, "
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id), "
    "FOREIGN KEY (word_id) REFERENCES words (id))")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_phrases(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, phrase_id INTEGER, score INTEGER,"
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id), "
    "FOREIGN KEY (phrase_id) REFERENCES phrases (id))")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_sents(id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "user_id INTEGER, sent_id INTEGER, score INTEGER,"
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id), "
    "FOREIGN KEY (sent_id) REFERENCES sents (id))")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_quests(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, quest_id INTEGER, score INTEGER,"
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id), "
    "FOREIGN KEY (quest_id) REFERENCES quests (id))")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user_session(id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "user_id INTEGER,"
    "task_id1 INTEGER,"
    "task_id2 INTEGER,"
    "task_id3 INTEGER,"
    "task_id4 INTEGER,"
    "task_id5 INTEGER,"
    "task_id6 INTEGER,"
    "task_id7 INTEGER,"
    "task_id8 INTEGER,"
    "task_id9 INTEGER,"
    "task_id10 INTEGER,"
    "task_id11 INTEGER,"
    "task_id12 INTEGER,"
    "task_id13 INTEGER,"
    "task_id14 INTEGER,"
    "task_id15 INTEGER,"
    "task_id16 INTEGER,"
    "score1 INTEGER,"
    "score2 INTEGER,"
    "score3 INTEGER,"
    "score4 INTEGER,"
    "score5 INTEGER,"
    "score6 INTEGER,"
    "score7 INTEGER,"
    "score8 INTEGER,"
    "score9 INTEGER,"
    "score10 INTEGER,"
    "score11 INTEGER,"
    "score12 INTEGER,"
    "score13 INTEGER,"
    "score14 INTEGER,"
    "score15 INTEGER,"
    "score16 INTEGER,"
    "date DATETIME, FOREIGN KEY (user_id) REFERENCES users (id))")

i = 0
for w in df['words']:
    path = f'../static/audio/words/{i}.mp3'
    cur.execute(f"INSERT INTO words VALUES({i}, '{w}','{path}')")
    # tts = gTTS(w, lang='ru', slow=False)
    # tts.save(path)
    i += 1
i = 0
for w in df['phrase1']:
    path = f'../static/audio/phrases/{i}.mp3'
    cur.execute(f"INSERT INTO phrases VALUES({i}, '{w}','{path}')")
    # tts = gTTS(w, lang='ru', slow=False)
    # tts.save(path)
    i += 1
for w in df['phrase2']:
    path = f'../static/audio/phrases/{i}.mp3'
    cur.execute(f"INSERT INTO phrases VALUES({i},  '{w}','{path}')")
    # tts = gTTS(w, lang='ru', slow=False)
    # tts.save(path)
    i += 1
i = 0
for w in df['sent1']:
    path = f'../static/audio/sents/{i}.mp3'
    cur.execute(f"INSERT INTO sents VALUES({i}, '{w}','{path}')")
    # tts = gTTS(w, lang='ru', slow=False)
    # tts.save(path)
    i += 1
for w in df['sent2']:
    path = f'../static/audio/sents/{i}.mp3'
    cur.execute(f"INSERT INTO sents VALUES({i},  '{w}','{path}')")
    # tts = gTTS(w, lang='ru', slow=False)
    # tts.save(path)
    i += 1
i = 0
for w in df['inf1']:
    path = f'../static/audio/infs/{i}.mp3'
    cur.execute(f"INSERT INTO infs VALUES({i}, '{w}','{path}')")
    # if type(w) != float:
    # tts = gTTS(w, lang='ru', slow=False)
    # tts.save(path)
    i += 1
for w in df['inf2']:
    path = f'../static/audio/infs/{i}.mp3'
    cur.execute(f"INSERT INTO infs VALUES({i},  '{w}','{path}')")
    # if type(w) != float:
    #     tts = gTTS(w, lang='ru', slow=False)
    #     tts.save(path)
    i += 1

i = 0
for w in df['quest1']:
    cur.execute(f"INSERT INTO quests VALUES({i}, '{w}')")
    i += 1
for w in df['quest2']:
    cur.execute(f"INSERT INTO quests VALUES({i}, '{w}')")
    i += 1
i = 0
for w in df['miss_sent1']:
    cur.execute(f"INSERT INTO miss_sents VALUES({i}, '{w}')")
    i += 1
for w in df['miss_sent2']:
    cur.execute(f"INSERT INTO miss_sents VALUES({i}, '{w}')")
    i += 1

con.commit()
# for row in cur.execute("SELECT id, type, text, path FROM exercise"):
#     print(row)
