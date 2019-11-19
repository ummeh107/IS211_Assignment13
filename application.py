
from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3 as lite
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['user'] = request.form['username']
            return redirect(url_for('dashboard'))
        error = 'admin & password is not correct!'        
        return render_template('login.html', error=error)
    else:        
        return render_template('login.html', error=error)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user' in session:
        students= []
        quizes = []
        students = query_fetch_data('select * from Students')
        print(students)
        quizes = query_fetch_data('select * from Quizzes')
        print(quizes)
        return render_template('dashboard.html', students = students, quizes=quizes)
    else:
        return redirect('/')    


@app.route('/student/add', methods=['GET'])
def student():
    if 'user' in session:
        return render_template('add_student.html')
    else:
        return redirect('/')    

@app.route('/student', methods=['POST'])
def add_student():
    id = request.form['id']
    first_name = request.form['f_name']
    last_name = request.form['l_name']

    if int(id) > 0 and first_name != '' and last_name != '':
        saved = query_fetch_data('insert into Students(id, first_name, last_name) values(?, ?, ?)', (int(id), first_name, last_name))
        if saved:
            return redirect('/dashboard') 
        else:
            return render_template('add_student.html',error='Not saved, Please try again!') 
    else:
        return render_template('add_student.html',error='Not valid students! ')

@app.route('/quiz/add', methods=['GET'])
def quiz():
    if 'user' in session:
        return render_template('add_quiz.html')
    else:
        return redirect('/') 

@app.route('/quiz', methods=['POST'])
def add_quiz():
    id = request.form['id']
    subject = request.form['subject']
    question = request.form['question']
    date = request.form['date']
    
    if int(id) > 0 and subject != '' and question != '' and date != None:
        saved = query_fetch_data('insert into Quizzes(id, subject, no_of_questions, date) values(?, ?, ?, ?)',(int(id), subject, question, date))
        if saved:
            return redirect('/dashboard')
        else:
            return render_template('add_quiz.html', error = 'Not saved, please try again!')
    else:
        return render_template('add_quiz.html', error='Not valid quiz!')                

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if request.method == 'GET':
        if 'user' in session:
            students = query_fetch_data('select id from Students')
            quiz = query_fetch_data('select id from Quizzes')
            return render_template('add_result.html', students=students, quiz = quiz)
        else:
            return redirect('/')
    elif request.method == 'POST':
        std_id = request.form['std_id']
        quiz_id = request.form['quiz_id']
        result = request.form['result']

        saved = query_fetch_data('insert into Student_Results(student_id, quiz_id, result) values (?, ?, ?)', (int(std_id), int(quiz_id), int(result)))
        if saved:
            return redirect('/dashboard') 
        else:
            return render_template('add_result.html',error='Not saved, Please try again!')

@app.route('/student/<id>', methods=['GET'])
def student_details(id):
    if 'user' in session:
        std = query_fetch_data('select * from Students where id=?',(id))
        rslt = query_fetch_data('select * from Student_Results inner join Quizzes on Student_Results.quiz_id = Quizzes.id where student_id=?', (id))
        return render_template('result.html', student=std, result = rslt)
    else:
        return redirect('/')


def query_fetch_data(query, item=None):
    conn = lite.connect('hw13.db')
    db = conn.cursor()
    print(item)
    if item == None:
        db.execute(query)
    elif len(item) == 1:
        try:
            db.execute(query, item)
            return db.fetchall()
        except:
            return False
    else:
        try:
            db.execute(query, item)
            conn.commit()
            return True
        except:
            return False
    return db.fetchall()



if __name__=='__main__':
    app.run(debug=True) 