from flask import Flask, render_template, request, redirect, flash
from maktabah import getResult
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config.from_pyfile('config.py')

@app.route('/', methods=['GET', 'POST'])
def index(): 
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.args.get('search'):
        start_time = time.time()
        search = request.args['search']
        print(search)
        if ('\u0600' <= search <= '\u06FF' or
            '\u0750' <= search <= '\u077F' or
            '\u08A0' <= search <= '\u08FF' or
            '\uFB50' <= search <= '\uFDFF' or
            '\uFE70' <= search <= '\uFEFF' or
            '\U00010E60' <= search <= '\U00010E7F' or
            '\U0001EE00' <= search <= '\U0001EEFF'):
            print("================START=======================")
            res = getResult(search)
            print("=====================END====================")
            print(res)
            len_result = len(res)
            total_time = (time.time() - start_time)
            return render_template('result.html', results = res, query = search, totalTime = total_time, lenResult = len_result)
        flash('ARABIC ONLY!', 'error')
        return redirect('/')
    else:
        return redirect('/')

@app.route('/result/detail', methods=['GET', 'POST'])
def detail():
    namakitab = request.args.get('kitab')
    halaman = request.args.get('hal')
    isikitab = request.args.get('data')
    return render_template('detail.html', namakitab=namakitab, halaman=halaman, isikitab=isikitab)

if __name__ == "__main__":
    app.run(debug=True) 