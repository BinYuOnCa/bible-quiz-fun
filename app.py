from flask import Flask, render_template, request
from quiz import quiz
import re
import os

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    # print(f'index....{request.method=}.')
    # print(f'index....{request.args=}.')
    # print(f'index....{request.form=}.')
    # print(f'index....{request.data=}.')
    # print(f'index....{request=}.')
    #
    # with open('request.dump', 'wb') as f:
    #     dump(('DUMP DATA',
    #           request.method, request.host_url,
    #           # request,
    #           'DUMP END', ),  f)
    #
    # print('Dumped to request.dump....')
    # print(f"in app.py: {os.getcwd()=}")
    # print(f"{os.path.realpath(__file__)=}")
    random_key = None
    # action = None
    quote_text = None
    book_name =  quiz.book_name

    if request.method == 'POST':
        action = request.form.get('action','')
        if action == 'key':
            random_key = quiz.rand_keyword()
            print(f"POST: {random_key=},{action=},{quote_text=}")
        elif action == 'result':
            user_input = request.form.get('user_input', '')
            random_key = quiz.active_key_word
            quote_text = quiz.quote_for_key(user_input)
            print(f"POST: {user_input=},{action=},{quote_text=}")

    return render_template('index.html',
                           user_input=random_key,
                           quote_txt=quote_text,
                           book_name=book_name,
                           )


if __name__ == '__main__':
    app.run(debug=True)