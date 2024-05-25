import json
from random import random, choice, shuffle

from flask import Flask, render_template, request, send_file, url_for, make_response, redirect

from controler.ex_controller import Ex

ex = Ex()

app = Flask(__name__)


@app.route('/reboot', methods=['GET'])
def reboot():
    """Set a new session cookie. The default cookie expires when the session ends."""
    user_id = ex.create_new_user()
    response = make_response(redirect('/'))
    response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
    return response


@app.route('/', methods=['GET'])
def index():
    """Set a new session cookie. The default cookie expires when the session ends."""
    user_id = request.cookies.get('user_id')
    if user_id is None:
        user_id = ex.create_new_user()
    response = make_response(render_template("index.html", id_=user_id, cookies=request.cookies))
    response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
    return response


@app.route('/word', methods=['GET', 'POST'])
def word():
    user_id = request.cookies.get('user_id')
    if request.method == 'POST':
        word_id = request.cookies.get('word_id')
        q = request.form['answer']
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_word_answer(user_id, word_id, int(answer))
        return redirect("/word")

    if request.method == 'GET':
        isend = False
        if user_id is None:
            user_id = ex.create_new_user()
        id_, w, p = ex.get_random_word_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            corr_count = int(ex.get_correct_word_count(user_id))
            incorr_count = int(ex.get_incorrect_word_count(user_id))
            all_count = int(ex.get_words_count())
            audio = url_for('static', filename=p)

        response = make_response(render_template('word.html',
                                                 aud=audio,
                                                 correct_answers=w,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 isend=isend,
                                                 incor=False
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("word_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)
        return response


@app.route('/word_incor', methods=['GET', 'POST'])
def quiz_incor():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('word_id')
        q = request.form['answer']
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_word_answer(user_id, word_id, int(answer))
        return redirect("/word_incor")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_incor_word_ids_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, w, p = ex.get_word_by_id(id_)
            corr_count = int(ex.get_correct_word_count(user_id))
            incorr_count = int(ex.get_incorrect_word_count(user_id))
            all_count = int(ex.get_words_count())
            audio = url_for('static', filename=p)
        response = make_response(render_template('word.html',
                                                 aud=audio,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=True,
                                                 isend=isend,
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("word_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/word_radio2', methods=['GET', 'POST'])
def word_radio2():
    user_id = request.cookies.get('user_id')
    if request.method == 'POST':
        word_id = request.cookies.get('word_id')
        q = request.form['answer']
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_radio2words_answer(user_id, word_id, int(answer))
        return redirect("/word_radio2")

    if request.method == 'GET':
        isend = False
        if user_id is None:
            user_id = ex.create_new_user()
        id_, w, p = ex.get_random_radio2word_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count, w1, w2 = None, 0, 1, 0, '', ''
        else:
            _r, wr, pr = ex.get_random_radio_word(id_)
            corr_count = int(ex.get_correct_radio2word_count(user_id))
            incorr_count = int(ex.get_incorrect_radio2word_count(user_id))
            all_count = int(ex.get_words_count())
            if round(random()) == 1:
                w1 = wr
                w2 = w
            else:
                w1 = w
                w2 = wr

            audio = url_for('static', filename=p)
        response = make_response(render_template('word_radio2.html',
                                                 aud=audio,
                                                 answer1=w1,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 answer2=w2,
                                                 isend=isend,
                                                 incor=False
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("word_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/word_radio2_incor', methods=['GET', 'POST'])
def word_radio2_incor():
    user_id = request.cookies.get('user_id')
    if request.method == 'POST':
        word_id = request.cookies.get('word_id')
        q = request.form['answer']
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_radio2words_answer(user_id, word_id, int(answer))
        return redirect("/word_radio2_incor")

    if request.method == 'GET':
        isend = False
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_incor_word2radio_ids_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count, w1, w2 = None, 0, 1, 0, '', ''
        else:
            id_, w, p = ex.get_word_by_id(id_)
            _r, wr, pr = ex.get_random_radio_word(id_)
            corr_count = int(ex.get_correct_radio2word_count(user_id))
            incorr_count = int(ex.get_incorrect_radio2word_count(user_id))
            all_count = int(ex.get_words_count())
            if round(random()) == 1:
                w1 = wr
                w2 = w
            else:
                w1 = w
                w2 = wr
            audio = url_for('static', filename=p)
        response = make_response(render_template('word_radio2.html',
                                                 aud=audio,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=True,
                                                 isend=isend,
                                                 answer1=w1,
                                                 answer2=w2
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("word_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz_radio4', methods=['GET', 'POST'])
def quiz_radio4():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('word_id')
        q = request.form['answer']
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_radio4words_answer(user_id, word_id, int(answer))
        return redirect("/quiz_radio4")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_sent_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, w, p = ex.get_random_radio4word_for_user(user_id)
            _r, wr, pr = ex.get_random_radio_word(id_)
            _r, wr1, pr1 = ex.get_random_radio_word(user_id)
            _r, wr2, pr2 = ex.get_random_radio_word(user_id)
            corr_count = int(ex.get_correct_radio4word_count(user_id))
            incorr_count = int(ex.get_incorrect_radio4word_count(user_id))
            all_count = int(ex.get_words_count())
            words = [w, wr1, wr2, wr]
            shuffle(words)
            w1, w2, w3, w4 = words

        audio = url_for('static', filename=p)
        response = make_response(render_template('quiz_radio4.html',
                                                 aud=audio,
                                                 answer1=w1,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 answer2=w2,
                                                 answer3=w3,
                                                 answer4=w4,
                                                 incor=False,
                                                 isend=isend
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("word_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz_radio4_incor', methods=['GET', 'POST'])
def quiz_radio4_incor():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('word_id')
        q = request.form['answer']
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_radio4words_answer(user_id, word_id, int(answer))
        return redirect("/quiz_radio4_incor")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_incor_word_ids_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, w, p = ex.get_random_word_for_user(user_id)
            _r, wr, pr = ex.get_random_radio_word(id_)
            _r, wr1, pr1 = ex.get_random_radio_word(user_id)
            _r, wr2, pr2 = ex.get_random_radio_word(user_id)
            corr_count = int(ex.get_correct_radio4word_count(user_id))
            incorr_count = int(ex.get_incorrect_radio4word_count(user_id))
            all_count = int(ex.get_words_count())
            words = [w, wr1, wr2, wr]
            shuffle(words)
            w1, w2, w3, w4 = words

        audio = url_for('static', filename=p)
        response = make_response(render_template('quiz1.html',
                                                 aud=audio,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=True,
                                                 isend=isend,
                                                 answer1=w1,
                                                 answer2=w2,
                                                 answer3=w3,
                                                 answer4=w4
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("quest_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz_add', methods=['GET', 'POST'])
def quiz_add():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('quest_id')
        q = request.form['answer']
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_miss_sents_answer(user_id, word_id, int(answer))
        return redirect("/quiz_add")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_word_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, sent, audio_path = ex.get_random_sent_for_user(user_id)
            miss_sent = ex.get_miss_sentence_by_id(id_)
            corr_count = int(ex.get_correct_miss_sents_count(user_id))
            incorr_count = int(ex.get_incorrect_miss_sents_count(user_id))
            all_count = int(ex.get_words_count())

        audio = url_for('static', filename=audio_path)
        response = make_response(render_template('quiz_add.html',
                                                 aud=audio,
                                                 correct_answers=sent,
                                                 miss_sent=miss_sent,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=False,
                                                 isend=isend
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("quest_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz_add_incor', methods=['GET', 'POST'])
def quiz_add_incor():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('quest_id')
        q = request.form['answer']
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_miss_sents_answer(user_id, word_id, int(answer))
        return redirect("/quiz_add_incor")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_incor_miss_sent_ids_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, sent, audio_path = ex.get_random_sent_for_user(user_id)
            miss_sent = ex.get_miss_sentence_by_id(id_)
            corr_count = int(ex.get_correct_miss_sents_count(user_id))
            incorr_count = int(ex.get_incorrect_miss_sents_count(user_id))
            all_count = int(ex.get_words_count())
            audio = url_for('static', filename=audio_path)
        response = make_response(render_template('quiz1.html',
                                                 aud=audio,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=True,
                                                 isend=isend,
                                                 miss_sent=miss_sent
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("quest_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz1', methods=['GET', 'POST'])
def quiz1():
    if request.method == 'POST':
        q = request.form['answer']
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('word_id')
        true_answer = ex.get_sent_by_id(word_id)
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_word_answer(user_id, word_id, int(answer))
        return redirect("/quiz1")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_word_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, sent, audio_path = ex.get_random_sent_for_user(user_id)
            corr_count = int(ex.get_correct_sent_count(user_id))
            incorr_count = int(ex.get_incorrect_sent_count(user_id))
            all_count = int(ex.get_sents_count())

            audio = url_for('static', filename=audio_path)
        response = make_response(render_template('quiz1.html',
                                                 aud=audio,
                                                 correct_answers=sent,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=False,
                                                 isend=isend
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)

        # response.set_cookie("true_answer", w, max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("word_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz1_incor', methods=['GET', 'POST'])
def quiz1_incor():
    if request.method == 'POST':
        q = request.form['answer']
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('word_id')
        true_answer = ex.get_sent_by_id(word_id)
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_word_answer(user_id, word_id, int(answer))
        return redirect("/quiz1_incor")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_incor_sent_ids_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, phrase, audio_path = ex.get_random_sent_for_user(user_id)
            corr_count = int(ex.get_correct_sent_count(user_id))
            incorr_count = int(ex.get_incorrect_sent_count(user_id))
            all_count = int(ex.get_sents_count())
            audio = url_for('static', filename=audio_path)
        response = make_response(render_template('quiz1.html',
                                                 aud=audio,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=True,
                                                 isend=isend
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("quest_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
    if request.method == 'POST':
        q = request.form['answer']
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('word_id')
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_word_answer(user_id, word_id, int(answer))
        return redirect("/quiz2")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_word_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, phrase, audio_path = ex.get_random_phrase_for_user(user_id)
            corr_count = int(ex.get_correct_phrase_count(user_id))
            incorr_count = int(ex.get_incorrect_phrase_count(user_id))
            all_count = int(ex.get_phrases_count())

            audio = url_for('static', filename=audio_path)
        response = make_response(render_template('quiz1.html',
                                                 aud=audio,
                                                 correct_answers=phrase,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=False,
                                                 isend=isend
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)

        # response.set_cookie("true_answer", w, max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("word_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz2_incor', methods=['GET', 'POST'])
def quiz2_incor():
    if request.method == 'POST':
        q = request.form['answer']
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('word_id')
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_word_answer(user_id, word_id, int(answer))
        return redirect("/quiz2_incor")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_incor_phrase_ids_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, phrase, audio_path = ex.get_random_phrase_for_user(user_id)
            corr_count = int(ex.get_correct_phrase_count(user_id))
            incorr_count = int(ex.get_incorrect_phrase_count(user_id))
            all_count = int(ex.get_phrases_count())
            audio = url_for('static', filename=audio_path)
        response = make_response(render_template('infs.html',
                                                 aud=audio,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=True,
                                                 isend=isend
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("quest_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quest', methods=['GET', 'POST'])
def quest():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('quest_id')
        q = request.form['answer']
        true_answer = ex.get_word_by_id(word_id)[1]
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_quest_answer(user_id, word_id, int(answer))
        return redirect("/quest")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_sent_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            id_, sent, audio_path = ex.get_random_sent_for_user(user_id)
            quest = ex.get_question_by_id(id_)
            corr_count = int(ex.get_correct_quest_count(user_id))
            incorr_count = int(ex.get_incorrect_quest_count(user_id))
            all_count = int(ex.get_words_count())

            audio = url_for('static', filename=audio_path)
        response = make_response(render_template('question.html',
                                                 aud=audio,
                                                 correct_answers=sent,
                                                 quest=quest,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=False,
                                                 isend=isend
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("quest_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz_quest_incor', methods=['GET', 'POST'])
def quiz_quest_incor():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('quest_id')
        q = request.form['answer']
        true_answer = ex.get_sent_by_id(word_id)
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_inf_answer(user_id, word_id, int(answer))
        return redirect("/quiz_quest_incor")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_incor_quests_ids_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            _, sent, audio_path = ex.get_random_sent_for_user(id_)
            quest = ex.get_question_by_id(id_)
            corr_count = int(ex.get_correct_quest_count(user_id))
            incorr_count = int(ex.get_incorrect_quest_count(user_id))
            all_count = int(ex.get_words_count())  # TODO
            audio = url_for('static', filename=audio_path)
        response = make_response(render_template('question.html',
                                                 aud=audio,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=True,
                                                 isend=isend,
                                                 quest=quest,
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("quest_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz_inf', methods=['GET', 'POST'])
def quiz_inf():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('quest_id')
        q = request.form['answer']
        true_answer = ex.get_sent_by_id(word_id)
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_inf_answer(user_id, word_id, int(answer))
        return redirect("/quiz_inf")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_infs_ids_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            _, inf_sent, audio_path = ex.get_random_inf_sent_for_inf_id(id_)
            corr_count = int(ex.get_correct_inf_count(user_id))
            incorr_count = int(ex.get_incorrect_inf_count(user_id))
            all_count = int(ex.get_infs_count())  # TODO
            audio = url_for('static', filename=audio_path)
        response = make_response(render_template('infs.html',
                                                 aud=audio,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=False,
                                                 isend=isend
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("quest_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/quiz_inf_incor', methods=['GET', 'POST'])
def quiz_inf_incor():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        word_id = request.cookies.get('quest_id')
        q = request.form['answer']
        true_answer = ex.get_sent_by_id(word_id)
        answer = q.lower().strip() == true_answer.lower().strip()
        ex.set_user_inf_answer(user_id, word_id, int(answer))
        return redirect("/quiz_inf_incor")

    if request.method == 'GET':
        isend = False
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()
        id_ = ex.get_random_incor_infs_ids_for_user(user_id)
        if id_ is None:
            isend = True
            audio, corr_count, all_count, incorr_count = None, 0, 1, 0
        else:
            _, inf_sent, audio_path = ex.get_random_inf_sent_for_inf_id(id_)
            corr_count = int(ex.get_correct_inf_count(user_id))
            incorr_count = int(ex.get_incorrect_inf_count(user_id))
            all_count = int(ex.get_infs_count())  # TODO
            audio = url_for('static', filename=audio_path)
        response = make_response(render_template('infs.html',
                                                 aud=audio,
                                                 corr_count=corr_count,
                                                 all_count=all_count,
                                                 incorr_count=incorr_count,
                                                 incor=True,
                                                 isend=isend
                                                 ))
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("quest_id", str(id_), max_age=60 * 60 * 24 * 365 * 2)

        return response


@app.route('/session', methods=['GET', 'POST'])
def session():
    if request.method == 'POST':
        answers = []
        user_id = request.cookies.get('user_id')
        session_data = [int(i) for i in request.cookies.get('session-data').split(',')]
        q1 = request.form['answer1']
        q2 = request.form['answer2']
        true_answer1 = ex.get_word_by_id(session_data[0])[1]
        true_answer2 = ex.get_word_by_id(session_data[1])[1]
        answers.append(q1.lower().strip() == true_answer1.lower().strip())
        answers.append(q2.lower().strip() == true_answer2.lower().strip())

        q3 = request.form['answer3']
        q4 = request.form['answer4']
        true_answer3 = ex.get_word_by_id(session_data[2])[1]
        true_answer4 = ex.get_word_by_id(session_data[3])[1]
        answers.append(q3.lower().strip() == true_answer3.lower().strip())
        answers.append(q4.lower().strip() == true_answer4.lower().strip())

        q5 = request.form['answer5']
        q6 = request.form['answer6']
        true_answer5 = ex.get_word_by_id(session_data[4])[1]
        true_answer6 = ex.get_word_by_id(session_data[5])[1]
        answers.append(q5.lower().strip() == true_answer5.lower().strip())
        answers.append(q6.lower().strip() == true_answer6.lower().strip())

        q7 = request.form['answer7']
        q8 = request.form['answer8']
        true_answer7 = ex.get_word_by_id(session_data[6])[1]
        true_answer8 = ex.get_word_by_id(session_data[7])[1]
        answers.append(q7.lower().strip() == true_answer7.lower().strip())
        answers.append(q8.lower().strip() == true_answer8.lower().strip())

        q9 = request.form['answer9']
        q10 = request.form['answer10']
        true_answer9 = ex.get_sent_by_id(session_data[8])
        true_answer10 = ex.get_sent_by_id(session_data[9])
        answers.append(q9.lower().strip() == true_answer9.lower().strip())
        answers.append(q10.lower().strip() == true_answer10.lower().strip())

        q11 = request.form['answer11']
        q12 = request.form['answer12']
        true_answer11 = ex.get_phrase_by_id(session_data[10])
        true_answer12 = ex.get_phrase_by_id(session_data[11])
        answers.append(q11.lower().strip() == true_answer11.lower().strip())
        answers.append(q12.lower().strip() == true_answer12.lower().strip())

        q13 = request.form['answer13']
        q14 = request.form['answer14']
        true_answer13 = ex.get_word_by_id(session_data[12])[1]
        true_answer14 = ex.get_word_by_id(session_data[13])[1]
        answers.append(q13.lower().strip() == true_answer13.lower().strip())
        answers.append(q14.lower().strip() == true_answer14.lower().strip())

        q15 = request.form['answer15']
        q16 = request.form['answer16']
        true_answer15 = ex.get_sent_by_id(session_data[14])
        true_answer16 = ex.get_sent_by_id(session_data[15])
        answers.append(q15.lower().strip() == true_answer15.lower().strip())
        answers.append(q16.lower().strip() == true_answer16.lower().strip())
        ex.set_user_session_answer(user_id, session_data, answers)
        answers = [int(a) for a in answers]
        ts = sum(answers)

        return make_response(render_template('result.html',
                                             test_results=answers,
                                             total_score=ts
                                             ))

    if request.method == 'GET':
        user_id = request.cookies.get('user_id')
        if user_id is None:
            user_id = ex.create_new_user()

        id_11, word11, audio_path11 = ex.get_random_word_for_user(-1)
        id_12, word12, audio_path12 = ex.get_random_word_for_user(-1)
        audio11 = url_for('static', filename=audio_path11)
        audio12 = url_for('static', filename=audio_path12)

        id_21, word21, audio_path21 = ex.get_random_word_for_user(-1)
        id_22, word22, audio_path22 = ex.get_random_word_for_user(-1)
        _r1, wr1, pr1 = ex.get_random_radio_word(-1)
        _r2, wr2, pr2 = ex.get_random_radio_word(-1)
        if round(random()) == 1:
            w1 = word21
            w2 = wr1
            w3 = word22
            w4 = wr2
        else:
            w1 = wr1
            w2 = word21
            w3 = wr2
            w4 = word22

        audio21 = url_for('static', filename=audio_path21)
        audio22 = url_for('static', filename=audio_path22)

        id_31, word31, audio_path31 = ex.get_random_word_for_user(-1)
        id_32, word32, audio_path32 = ex.get_random_word_for_user(-1)

        _r31, wr31, pr31 = ex.get_random_radio_word(id_31)
        _r32, wr32, pr32 = ex.get_random_radio_word(id_31)
        _r33, wr33, pr33 = ex.get_random_radio_word(id_31)

        _r34, wr34, pr34 = ex.get_random_radio_word(id_32)
        _r35, wr35, pr34 = ex.get_random_radio_word(id_32)
        _r36, wr36, pr36 = ex.get_random_radio_word(id_32)

        words1 = [word31, wr31, wr32, wr33]
        words2 = [word32, wr34, wr35, wr36]
        shuffle(words1)
        shuffle(words2)

        w31_1, w31_2, w31_3, w31_4 = words1
        w32_1, w32_2, w32_3, w32_4 = words2

        audio31 = url_for('static', filename=audio_path31)
        audio32 = url_for('static', filename=audio_path32)

        id_41, sent41, audio_path41 = ex.get_random_sent_for_user(-1)
        miss_sent41 = ex.get_miss_sentence_by_id(id_41)

        id_42, sent42, audio_path42 = ex.get_random_sent_for_user(-1)
        miss_sent42 = ex.get_miss_sentence_by_id(id_42)

        audio41 = url_for('static', filename=audio_path41)
        audio42 = url_for('static', filename=audio_path42)

        id_51, sent51, audio_path51 = ex.get_random_sent_for_user(-1)
        id_52, sent52, audio_path52 = ex.get_random_sent_for_user(-1)
        audio51 = url_for('static', filename=audio_path51)
        audio52 = url_for('static', filename=audio_path52)

        id_61, phrase61, audio_path61 = ex.get_random_phrase_for_user(-1)
        id_62, phrase62, audio_path62 = ex.get_random_phrase_for_user(-1)
        audio61 = url_for('static', filename=audio_path61)
        audio62 = url_for('static', filename=audio_path62)

        id_71, sent71, audio_path71 = ex.get_random_sent_for_user(-1)
        quest71 = ex.get_question_by_id(id_71)
        id_72, sent72, audio_path72 = ex.get_random_sent_for_user(-1)
        quest72 = ex.get_question_by_id(id_72)
        audio71 = url_for('static', filename=audio_path71)
        audio72 = url_for('static', filename=audio_path72)

        id_81 = ex.get_random_infs_ids_for_user(-1)
        id_82 = ex.get_random_infs_ids_for_user(-1)
        _, inf_sent81, audio_path81 = ex.get_random_inf_sent_for_inf_id(id_81)
        _, inf_sent82, audio_path82 = ex.get_random_inf_sent_for_inf_id(id_82)
        audio81 = url_for('static', filename=audio_path81)
        audio82 = url_for('static', filename=audio_path82)

        response = make_response(render_template('session.html',
                                                 aud11=audio11,
                                                 aud12=audio12,
                                                 aud21=audio21,
                                                 aud22=audio22,
                                                 aud31=audio31,
                                                 aud32=audio32,
                                                 aud41=audio41,
                                                 aud42=audio42,
                                                 aud51=audio51,
                                                 aud52=audio52,
                                                 aud61=audio61,
                                                 aud62=audio62,
                                                 aud71=audio71,
                                                 aud72=audio72,
                                                 aud81=audio81,
                                                 aud82=audio82,
                                                 answer21=w1,
                                                 answer22=w2,
                                                 answer23=w3,
                                                 answer24=w4,
                                                 answer30=w31_1,
                                                 answer31=w31_2,
                                                 answer32=w31_3,
                                                 answer33=w31_4,
                                                 answer300=w32_1,
                                                 answer34=w32_2,
                                                 answer35=w32_3,
                                                 answer36=w32_4,
                                                 miss_sent41=miss_sent41,
                                                 miss_sent42=miss_sent42,
                                                 quest71=quest71,
                                                 quest72=quest72
                                                 ))
        ids = [id_11, id_12, id_21, id_22, id_31, id_32, id_41, id_42, id_51, id_52, id_61, id_62, id_71, id_72, id_81,
               id_82]
        ids = [str(i) for i in ids]
        response.set_cookie("user_id", str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        response.set_cookie("session-data", ','.join(ids), max_age=60 * 60 * 24 * 365 * 2)

        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
