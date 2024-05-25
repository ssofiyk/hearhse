import datetime
import sqlite3

import pandas as pd


class Dao:
    def __init__(self):
        self.con = sqlite3.connect("db.db", check_same_thread=False)

    def __del__(self):
        self.con.close()

    def get_question(self, table_name, id):
        cur = self.con.cursor()
        cur.execute(f"Select * from {table_name} where id = {id}")
        return cur.fetchone()

    def count_question(self, table_name):
        cur = self.con.cursor()
        cur.execute(f"Select count(*) from {table_name}")
        return int(cur.fetchone()[0])

    def create_new_user(self, id):
        cur = self.con.cursor()
        cur.execute(f"Insert into users values ({id})")
        self.con.commit()
        return id

    def get_max_user_id(self):
        cur = self.con.cursor()
        cur.execute(f'SELECT Max(id) FROM users')
        id_ = cur.fetchone()[0]
        if id_ is None:
            id_ = 0
        return int(id_)

    def get_incorrect_words_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f"""select distinct user_words.word_id
from user_words
where (word_id not in (Select word_id from user_words where score == 1)
    and user_id == {id} and word_id in (select word_id
                                     from user_words
                                     where user_id == {id}
                                       and score == 0
                                     group by word_id
                                     having count(*) <= 3))""")
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_correct_words_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_words where score == 1 and user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_correct_radio2words_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_radio2words where score == 1 and user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_correct_miss_sents_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_miss_sents where score == 1 and user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_all_words_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_words where user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_all_radio2words_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_radio2words where user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_all_radio4words_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_radio4words where user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_incorrect_sents_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT sent_id from user_sents where score == 0 and user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_correct_sents_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT sent_id from user_sents where score == 1 and user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_all_sents_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT sent_id from user_sents where user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_incorrect_phrases_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT phrase_id from user_phrases where score == 0 and user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_correct_phrases_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT phrase_id from user_phrases where score == 1 and user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_all_phrases_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT phrase_id from user_phrases where user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_word_by_id(self, id_):
        cur = self.con.cursor()
        cur.execute(f"Select id, text, path from words where id = {id_}")
        return cur.fetchone()

    def set_user_word_answer(self, user_id, word_id, answer, dt):
        cur = self.con.cursor()
        q = f"Insert into user_words values (NULL,{user_id},{word_id},{answer},?)"
        print(q)
        cur.execute(q, (dt,))
        self.con.commit()
        return id

    def set_user_radio2words_answer(self, user_id, word_id, answer, dt):
        cur = self.con.cursor()
        q = f"Insert into user_radio2words values (NULL,{user_id},{word_id},{answer},?)"
        print(q)
        cur.execute(q, (dt,))
        self.con.commit()
        return id

    def set_user_phrase_answer(self, user_id, word_id, answer, dt):
        cur = self.con.cursor()
        q = f"Insert into user_phrases values (NULL,{user_id},{word_id},{answer},?)"
        print(q)
        cur.execute(q, (dt,))
        self.con.commit()
        return id

    def set_user_sent_answer(self, user_id, word_id, answer, dt):
        cur = self.con.cursor()
        q = f"Insert into user_sents values (NULL,{user_id},{word_id},{answer},?)"
        print(q)
        cur.execute(q, (dt,))
        self.con.commit()
        return id

    def get_phrase_by_id(self, id_):
        cur = self.con.cursor()
        cur.execute(f"Select text from phrases where id = {id_}")
        return cur.fetchone()[0]

    def get_sent_by_id(self, id_):
        cur = self.con.cursor()
        cur.execute(f"Select text from sents where id = {id_}")
        return cur.fetchone()[0]

    def get_quest_by_id(self, id_):
        cur = self.con.cursor()
        cur.execute(f"Select text from quests where id = {id_}")
        return cur.fetchone()[0]

    def get_miss_sentence_by_id(self, id_):
        cur = self.con.cursor()
        cur.execute(f"Select text from miss_sents where id = {id_}")
        return cur.fetchone()[0]

    def get_avail_infs_ids(self, user_id):
        cur = self.con.cursor()
        cur.execute(f"""Select id from infs where text is not 'nan' and id not in (SELECT DISTINCT word_id from user_inf where user_id == {user_id})""")
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_infs_by_id(self, id_):
        cur = self.con.cursor()
        cur.execute(f"Select text from infs where id = {id_}")
        return cur.fetchone()[0]

    def get_incorrect_radio2words_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f"""select distinct word_id
        from user_radio2words
        where (word_id not in (Select word_id from user_radio2words where score == 1)
            and user_id == {id} and word_id in (select word_id
                                             from user_radio2words
                                             where user_id == {id}
                                               and score == 0
                                             group by word_id
                                             having count(*) <= 3))
        """)
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_incorrect_miss_sents_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f"""select distinct word_id
        from user_miss_sents
        where (word_id not in (Select word_id from user_miss_sents where score == 1)
            and user_id == {id} and word_id in (select word_id
                                             from user_miss_sents
                                             where user_id == {id}
                                               and score == 0
                                             group by word_id
                                             having count(*) <= 3))
        """)
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def set_user_miss_sents_answer(self, user_id, word_id, answer, dt):
        cur = self.con.cursor()
        q = f"Insert into user_miss_sents values (NULL,{user_id},{word_id},{answer},?)"
        print(q)
        cur.execute(q, (dt,))
        self.con.commit()
        return id

    def set_user_quest_answer(self, user_id, word_id, answer, dt):
        cur = self.con.cursor()
        q = f"Insert into user_quest values (NULL,{user_id},{word_id},{answer},?)"
        print(q)
        cur.execute(q, (dt,))
        self.con.commit()
        return id

    def get_incorrect_quest_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f"""select distinct word_id
        from user_quest
        where (word_id not in (Select word_id from user_quest where score == 1)
            and user_id == {id} and word_id in (select word_id
                                             from user_quest
                                             where user_id == {id}
                                               and score == 0
                                             group by word_id
                                             having count(*) <= 3))
        """)
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_correct_quest_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_quest where score == 1 and user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_correct_inf_sents_by_user_id(self, id_):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_inf where score == 1 and user_id == {id_}')
        ids = cur.fetchall()
        ids = [int(id_[0]) for id_ in ids]
        return ids

    def get_incorrect_inf_sents_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f"""select distinct word_id
                from user_inf
                where (word_id not in (Select word_id from user_inf where score == 1)
                    and user_id == {id} and word_id in (select word_id
                                                     from user_inf
                                                     where user_id == {id}
                                                       and score == 0
                                                     group by word_id
                                                     having count(*) <= 3))
                """)
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def set_user_inf_sents_answer(self, user_id, word_id, answer, dt):
        cur = self.con.cursor()
        q = f"Insert into user_inf values (NULL,{user_id},{word_id},{answer},?)"
        print(q)
        cur.execute(q, (dt,))
        self.con.commit()
        return id

    def get_all_inf_sents_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_inf where user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def count_inf_sents(self, table_name):
        cur = self.con.cursor()
        cur.execute(f"Select count(*) from {table_name}")
        return int(cur.fetchone()[0])

    def get_inf(self, table_name, id):
        cur = self.con.cursor()
        cur.execute(f"Select * from {table_name} where id = {id}")
        return cur.fetchone()

    def get_incorrect_radio4words_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f"""select distinct word_id
                from user_radio4words
                where (word_id not in (Select word_id from user_radio4words where score == 1)
                    and user_id == {id} and word_id in (select word_id
                                                     from user_radio4words
                                                     where user_id == {id}
                                                       and score == 0
                                                     group by word_id
                                                     having count(*) <= 3))
                """)
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def get_correct_radio4words_by_user_id(self, id):
        cur = self.con.cursor()
        cur.execute(f'SELECT word_id from user_radio4words where score == 1 and user_id == {id}')
        ids = cur.fetchall()
        ids = [int(id[0]) for id in ids]
        return ids

    def set_user_radio4words_answer(self, user_id, word_id, answer, dt):
        cur = self.con.cursor()
        q = f"Insert into user_radio4words values (NULL,{user_id},{word_id},{answer},?)"
        print(q)
        cur.execute(q, (dt,))
        self.con.commit()
        return id

    def set_user_session_answer(self, user_id, ids, scores, dt):
        cur = self.con.cursor()
        ids = ','.join([str(i) for i in ids])
        scores = ','.join([str(int(i)) for i in scores])
        q = f"Insert into user_session values (NULL,{user_id},{ids},{scores},?)"
        cur.execute(q, (dt,))
        self.con.commit()
        return id

    def get_user_last_session(self, user_id):
        cur = self.con.cursor()
        cur.execute(f"Select * from user_session where user_id = {user_id} order by date DESC LIMIT 1")
        return cur.fetchone()
