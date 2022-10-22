from flask import Flask

app = Flask(__name__)

'''creating index route so
when we browse to the URL, we
dont immediately just 404
'''

@app.route('/')
def inde():
    return "hello, world"
