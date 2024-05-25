import datetime

from dao.dao import Dao
import random


class Ex:
    def __init__(self):
        self.db = Dao()

    def get_random_word(self):
        t_name = 'words'
        count = self.db.count_question(t_name)
        id = random.randint(0, count - 1)
        _, w, p = self.db.get_question(t_name, id)
        return w, p[10:]

    def get_random_word_for_user(self, id):
        t_name = 'words'
        ban_words_ids = self.db.get_all_words_by_user_id(id)
        words_count = self.db.count_question(t_name)
        words_count_2 = words_count // 2
        if len(ban_words_ids) < words_count_2:
            free_words_ids = [item for item in range(words_count_2) if item not in ban_words_ids]
        else:
            free_words_ids = [item for item in range(words_count_2, words_count) if item not in ban_words_ids]
        if len(free_words_ids) == 0:
            return None, None, None
        id_, w, p = self.db.get_question(t_name, random.choice(free_words_ids))
        return id_, w, p[10:]

    def get_random_radio2word_for_user(self, id):
        t_name = 'words'
        ban_words_ids = self.db.get_all_radio2words_by_user_id(id)
        words_count = self.db.count_question(t_name)
        words_count_2 = words_count // 2
        if len(ban_words_ids) < words_count_2:
            free_words_ids = [item for item in range(words_count_2) if item not in ban_words_ids]
        else:
            free_words_ids = [item for item in range(words_count_2, words_count) if item not in ban_words_ids]
        if len(free_words_ids) == 0:
            return None, None, None
        id_, w, p = self.db.get_question(t_name, random.choice(free_words_ids))
        return id_, w, p[10:]

    def get_random_radio4word_for_user(self, id):
        t_name = 'words'
        ban_words_ids = self.db.get_all_radio4words_by_user_id(id)
        words_count = self.db.count_question(t_name)
        words_count_2 = words_count // 2
        if len(ban_words_ids) < words_count_2:
            free_words_ids = [item for item in range(words_count_2) if item not in ban_words_ids]
        else:
            free_words_ids = [item for item in range(words_count_2, words_count) if item not in ban_words_ids]
        if len(free_words_ids) == 0:
            return None, None, None
        id_, w, p = self.db.get_question(t_name, random.choice(free_words_ids))
        return id_, w, p[10:]

    def is_user_has_free_words(self, id):
        ban_words_ids = self.db.get_all_words_by_user_id(id)
        words_count = self.db.count_question('words')
        # if ban_words_ids == words_count:

    def get_correct_word_count(self, id):
        return len(self.db.get_correct_words_by_user_id(id))

    def get_correct_radio2word_count(self, id):
        return len(self.db.get_correct_radio2words_by_user_id(id))

    def get_correct_miss_sents_count(self, id):
        return len(self.db.get_correct_miss_sents_by_user_id(id))

    def get_correct_quest_count(self, id):
        return len(self.db.get_correct_quest_by_user_id(id))

    def get_incorrect_word_count(self, id):
        return len(self.db.get_incorrect_words_by_user_id(id))

    def get_incorrect_radio2word_count(self, id):
        return len(self.db.get_incorrect_radio2words_by_user_id(id))

    def get_incorrect_miss_sents_count(self, id):
        return len(self.db.get_incorrect_miss_sents_by_user_id(id))

    def get_incorrect_quest_count(self, id):
        return len(self.db.get_incorrect_quest_by_user_id(id))

    def get_words_count(self):
        return self.db.count_question('words')

    def get_random_phrase(self):
        t_name1 = 'phrases'
        count = self.db.count_question(t_name1)
        id = random.randint(0, count - 1)
        _, ph, p = self.db.get_question(t_name1, id)
        return ph, p[10:]

    def get_random_phrase_for_user(self, id):
        t_name1 = 'phrases'
        ban_phrases_ids = self.db.get_all_phrases_by_user_id(id)
        phrases_count = self.db.count_question(t_name1)
        phrases_count_2 = phrases_count // 2
        if len(ban_phrases_ids) < phrases_count_2:
            free_phrases_ids = [item for item in range(phrases_count_2) if item not in ban_phrases_ids]
        else:
            free_phrases_ids = [item for item in range(phrases_count_2, phrases_count) if item not in ban_phrases_ids]
        if len(free_phrases_ids) == 0:
            return None, None, None
        id_, w, p = self.db.get_question(t_name1, random.choice(free_phrases_ids))
        return id_, w, p[10:]

    def is_user_has_free_phrases(self, id):
        ban_phrases_ids = self.db.get_all_phrases_by_user_id(id)
        phrases_count = self.db.count_question('phrases')

    def get_correct_phrase_count(self, id):
        return len(self.db.get_correct_phrases_by_user_id(id))

    def get_incorrect_phrase_count(self, id):
        return len(self.db.get_incorrect_phrases_by_user_id(id))

    def get_phrases_count(self):
        return self.db.count_question('phrases')

    def get_random_sent(self):
        t_name = 'sents'
        count = self.db.count_question(t_name)
        id = random.randint(0, count - 1)
        _, s, p = self.db.get_question(t_name, id)
        return s, p[10:]

    def get_random_sent_for_user(self, id):
        t_name1 = 'sents'
        ban_sents_ids = self.db.get_all_sents_by_user_id(id)
        sents_count = self.db.count_question(t_name1)
        sents_count_2 = sents_count // 2
        if len(ban_sents_ids) < sents_count_2:
            free_sents_ids = [item for item in range(sents_count_2) if item not in ban_sents_ids]
        else:
            free_sents_ids = [item for item in range(sents_count_2, sents_count) if item not in ban_sents_ids]
        if len(free_sents_ids) == 0:
            return None, None, None
        id_, w, p = self.db.get_question(t_name1, random.choice(free_sents_ids))
        return id_, w, p[10:]

    def is_user_has_free_sents(self, id):
        ban_phrases_ids = self.db.get_all_sents_by_user_id(id)
        phrases_count = self.db.count_question('sents')

    def get_correct_sent_count(self, id):
        return len(self.db.get_correct_sents_by_user_id(id))

    def get_incorrect_sent_count(self, id):
        return len(self.db.get_incorrect_sents_by_user_id(id))

    def get_sents_count(self):
        return self.db.count_question('sents')

    def create_new_user(self):
        max_id = self.db.get_max_user_id()
        self.db.create_new_user(max_id + 1)
        return max_id + 1

    def set_user_word_answer(self, user_id, word_id, score):
        self.db.set_user_word_answer(user_id, word_id, score, datetime.datetime.now())

    def set_user_phrase_answer(self, user_id, word_id, score):
        self.db.set_user_phrase_answer(user_id, word_id, score, datetime.datetime.now())

    def set_user_sent_answer(self, user_id, word_id, score):
        self.db.set_user_word_answer(user_id, word_id, score, datetime.datetime.now())

    def set_user_radio2words_answer(self, user_id, word_id, score):
        self.db.set_user_radio2words_answer(user_id, word_id, score, datetime.datetime.now())

    def set_user_quest_answer(self, user_id, word_id, score):
        self.db.set_user_quest_answer(user_id, word_id, score, datetime.datetime.now())

    def set_user_miss_sents_answer(self, user_id, word_id, score):
        self.db.set_user_miss_sents_answer(user_id, word_id, score, datetime.datetime.now())

    def get_word_by_id(self, id_):
        return self.db.get_word_by_id(id_)

    def get_phrase_by_id(self, id_):
        return self.db.get_phrase_by_id(id_)

    def get_sent_by_id(self, id_):
        return self.db.get_sent_by_id(id_)

    def get_random_radio_word(self, id_):
        t_name = 'words'
        count = self.db.count_question(t_name)
        id_r = random.choice([i for i in range(0, count - 1) if i not in [id_]])
        _r, wr, pr = self.db.get_question(t_name, id_r)
        return _r, wr, pr[10:]

    def get_question_by_id(self, id_):
        return self.db.get_quest_by_id(id_)

    def get_miss_sentence_by_id(self, id_):
        return self.db.get_miss_sentence_by_id(id_)

    def get_infs_by_id(self, id_):
        return self.db.get_infs_by_id(id_)

    def get_random_inf(self):
        t_name = 'infs'
        count = self.db.count_question(t_name)
        id = random.randint(0, count - 1)
        _, inf, p = self.db.get_question(t_name, id)
        return inf, p[10:]

    def get_random_inf_sent_for_inf_id(self, id_):
        t_name1 = 'infs'
        id_, w, p = self.db.get_inf(t_name1, id_)
        return id_, w, p[10:]

    def get_inf_sent_by_id(self, id):
        t_name1 = 'infs'
        ban_inf_sents_ids = self.db.get_all_inf_sents_by_user_id(id)
        inf_sents_count = self.db.count_inf_sents(t_name1)
        inf_sents_count_2 = inf_sents_count // 2
        if len(ban_inf_sents_ids) < inf_sents_count_2:
            free_inf_sents_ids = [item for item in range(inf_sents_count_2) if item not in ban_inf_sents_ids]
        else:
            free_inf_sents_ids = [item for item in range(inf_sents_count_2, inf_sents_count) if
                                  item not in ban_inf_sents_ids]
        if len(free_inf_sents_ids) == 0:
            free_inf_sents_ids = self.db.get_incorrect_inf_sents_by_user_id(id)
        id_, w, p = self.db.get_inf(t_name1, random.choice(free_inf_sents_ids))
        return id_, w, p[10:]

    def get_correct_inf_count(self, user_id):
        return len(self.db.get_correct_inf_sents_by_user_id(user_id))

    def get_incorrect_inf_count(self, user_id):
        return len(self.db.get_incorrect_inf_sents_by_user_id(user_id))

    def set_user_inf_answer(self, user_id, word_id, score):
        self.db.set_user_inf_sents_answer(user_id, word_id, score, datetime.datetime.now())

    def get_random_incor_infs_ids_for_user(self, user_id):
        ids = self.db.get_incorrect_inf_sents_by_user_id(user_id)
        if len(ids) > 0:
            return random.choice(ids)
        return None

    def get_random_incor_miss_sent_ids_for_user(self, user_id):
        ids = self.db.get_incorrect_miss_sents_by_user_id(user_id)
        if len(ids) > 0:
            return random.choice(ids)
        return None

    def get_random_incor_quests_ids_for_user(self, user_id):
        ids = self.db.get_incorrect_quest_by_user_id(user_id)
        if len(ids) > 0:
            return random.choice(ids)
        return None

    def get_random_incor_word_ids_for_user(self, user_id):
        ids = self.db.get_incorrect_words_by_user_id(user_id)
        if len(ids) > 0:
            return random.choice(ids)
        return None

    def get_random_incor_sent_ids_for_user(self, user_id):
        ids = self.db.get_incorrect_sents_by_user_id(user_id)
        if len(ids) > 0:
            return random.choice(ids)
        return None

    def get_random_incor_phrase_ids_for_user(self, user_id):
        ids = self.db.get_incorrect_phrases_by_user_id(user_id)
        if len(ids) > 0:
            return random.choice(ids)
        return None

    def get_random_infs_ids_for_user(self, user_id):
        ids = self.db.get_avail_infs_ids(user_id)
        if len(ids) > 0:
            return random.choice(ids)
        return None

    def get_infs_count(self):
        return self.db.count_question('infs')

    def get_random_infs_ids(self):
        pass

    def get_correct_radio4word_count(self, id):
        return len(self.db.get_correct_radio4words_by_user_id(id))

    def get_incorrect_radio4word_count(self, id):
        return len(self.db.get_incorrect_radio4words_by_user_id(id))

    def set_user_radio4words_answer(self, user_id, word_id, score):
        self.db.set_user_radio4words_answer(user_id, word_id, score, datetime.datetime.now())

    def set_user_session_answer(self, user_id, ids, scores):
        self.db.set_user_session_answer(user_id, ids, scores, datetime.datetime.now())

    def get_random_incor_word2radio_ids_for_user(self, user_id):
        ids = self.db.get_incorrect_radio2words_by_user_id(user_id)
        if len(ids) > 0:
            return random.choice(ids)
        return None
