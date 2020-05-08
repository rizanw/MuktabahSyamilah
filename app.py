from flask import Flask, render_template, request, redirect
from maktabah import getResult
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index(): 
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.args.get('search'):
        start_time = time.time()
        search = request.args['search']
        print(search)
        print("================START=======================")
        res = getResult(search)
        print("=====================END====================")
        print(res)
        len_result = len(res)
        total_time = (time.time() - start_time)
        return render_template('result.html', results = res, query = search, totalTime = total_time, lenResult = len_result)
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True) 