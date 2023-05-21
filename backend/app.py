from flask import Flask, jsonify
import service
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/*')  # 注册CORS, "/*" 允许访问所有api


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/thread/wordcloud')
def thread_wordcloud():
    res = service.get_thread_wordcount()
    return jsonify({'data': res})


@app.route('/post/wordcloud')
def post_wordcloud():
    res = service.get_post_wordcount()
    return jsonify({'data': res})


@app.route('/comment/wordcloud')
def comment_wordcloud():
    res = service.get_comment_wordcount()
    return jsonify({'data': res})


@app.route('/yesterday/post')
def yesterday_post():
    res = service.get_yesterday_post()
    return jsonify({'data': res})


@app.route('/yesterday/comment')
def yesterday_comment():
    res = service.get_yesterday_comment()
    return jsonify({'data': res})


@app.route('/post/ip')
def post_ip():
    res = service.get_post_ip()
    return jsonify({'data': res})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
