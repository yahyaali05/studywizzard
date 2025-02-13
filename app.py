import os
import random
import sqlite3
import db
from db import (
    get_db_con, 
    get_flashcards_for_user,
    initialize_categories, 
    username_exists, 
    register_user
)
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='geheimschluessel',  
    DATABASE=os.path.join(app.instance_path, 'studywizards.db')  
)
@app.before_request
def init_app_db():
    db.init_db()

app.teardown_appcontext(db.close_db_con)



@app.route('/logout')
def logout():
    session.clear()  
    flash('Du hast dich erfolgreich ausgeloggt!', 'success')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_id = db.check_user_credentials(username, password)
        
        if user_id:
            flash('Erfolgreich eingeloggt!', 'success')
            session['user_id'] = user_id
            return redirect(url_for('index'))
        else:
            flash('Ungültige Anmeldedaten. Versuche es erneut.', 'danger')
    
    return render_template('login.html')

@app.route('/insert/sample')
def run_insert_sample():
    db.init_db()
    if 'user_id' in session:
        user_id = session['user_id']
        db_con = get_db_con()
        db.insert_sample_for_user(user_id)
        initialize_categories(db_con, user_id)
        return redirect(url_for('select_grade'))

        
    flash('Du musst eingeloggt sein, um diese Aktion auszuführen.', 'danger')
    return redirect(url_for('login'))

@app.route('/view_flashcards')
def view_flashcards():
   

    user_id = session.get('user_id')
    if user_id is None:
        flash('Du musst eingeloggt sein, um deine Karteikarten zu sehen.', 'danger')
        return redirect(url_for('login'))

    category = request.args.get('category')
    grade_level = request.args.get('grade_level')
    shuffle = request.args.get('shuffle')  # Check if shuffle is requested


    db_con = get_db_con()

    # Fetch flashcards based on filters
    unknown_flashcards = db_con.execute('''
        SELECT id, category, question, answer
        FROM flashcards
        WHERE user_id = ? AND is_learned = 0
          AND category = ? AND grade_level = ?
        ORDER BY id
    ''', (user_id, category, grade_level)).fetchall()

    known_flashcards = db_con.execute('''
        SELECT id, category, question, answer
        FROM flashcards
        WHERE user_id = ? AND is_learned = 1
          AND category = ? AND grade_level = ?
        ORDER BY id
    ''', (user_id, category, grade_level)).fetchall()
    if shuffle == "true":

        unknown_flashcards = list(unknown_flashcards)
        random.shuffle(unknown_flashcards)
    return render_template(
        'view_flashcards.html',
        unknown_flashcards=unknown_flashcards,
        known_flashcards=known_flashcards,
        selected_category=category,
        selected_grade_level=grade_level
    )



@app.route('/select_grade', methods=['GET', 'POST'])
def select_grade():
    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um fortzufahren.', 'danger')
        return redirect(url_for('login'))

    grades = ["7", "8", "9", "10"]  # Define available grade levels

    if request.method == 'POST':
        selected_grade = request.form.get('grade_level')
        session['selected_grade'] = selected_grade
        return redirect(url_for('select_category'))  # Redirect to category selection

    return render_template('select_grade.html', grades=grades)



@app.route('/select_category', methods=['GET', 'POST'])
def select_category():
    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um fortzufahren.', 'danger')
        return redirect(url_for('login'))
    
    db_con = get_db_con()

    # Fetch categories from the database
    user_id = session['user_id']

    categories = db_con.execute('SELECT name FROM categories WHERE user_id = ?', (user_id,)).fetchall()
    categories = [row['name'] for row in categories] 

    if request.method == 'POST':
        new_category = request.form.get('new_category')
        if new_category:
            try:
                db_con.execute('INSERT INTO categories (name, user_id) VALUES (?, ?)', (new_category, user_id))
                db_con.commit()
                flash('New category added successfully!', 'success')
            except Exception as e:
                flash('Category already exists or invalid input.', 'danger')
            return redirect(url_for('select_category'))

        selected_category = request.form.get('category')
        session['selected_category'] = selected_category

        # Redirect to view_flashcards with both filters
        return redirect(url_for(
            'view_flashcards',
            category=selected_category,
            grade_level=session.get('selected_grade')
        ))

    return render_template('select_category.html', categories=categories)



@app.route('/select_flashcard_filters', methods=['GET', 'POST'])
def select_flashcard_filters():
    # db.init_db()
    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um fortzufahren.', 'danger')
        return redirect(url_for('login'))
    
    db_con = get_db_con()

    # Available categories (update as needed)
    categories = db_con.execute('SELECT name FROM categories').fetchall()
    categories = [row['name'] for row in categories] 
    if request.method == 'POST':
        new_category = request.form.get('new_category')
        if new_category:
            try:
                db_con.execute('INSERT INTO categories (name) VALUES (?)', (new_category,))
                db_con.commit()
                flash('New category added successfully!', 'success')
            except Exception as e:
                flash('Category already exists or invalid input.', 'danger')
        selected_category = request.form.get('category')
        selected_grade = request.form.get('grade_level')

        session['selected_category'] = selected_category
        session['selected_grade'] = selected_grade

        # Redirect to view_flashcards with filters as query parameters
        return redirect(url_for(
            'view_flashcards',
            category=selected_category,
            grade_level=selected_grade
        ))

    return render_template('select_flashcard_filters.html', categories=categories)

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            register_user(username, password)
            flash('Registrierung erfolgreich! Bitte logge dich ein.', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('register.html')

@app.route('/create_flashcard', methods=['GET', 'POST'])
def create_flashcard():
    if 'user_id' not in session:
        flash('Du musst eingeloggt sein, um eine Karteikarte zu erstellen.', 'danger')
        return redirect(url_for('login'))
    db_con = get_db_con()
    
    categories = db_con.execute('SELECT name FROM categories').fetchall()
    categories = [row['name'] for row in categories] 

    if request.method == 'POST':
        # Extract form data
        question = request.form['question']
        answer = request.form['answer']
        category = request.form['category']
        grade_level = request.form['grade_level']

        # Insert flashcard into the database
        user_id = session['user_id']
        db = get_db_con()
        db.execute('''
            INSERT INTO flashcards (user_id, question, answer, category, grade_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, question, answer, category, grade_level))
        db.commit()

        flash('Karteikarte erfolgreich erstellt!', 'success')
        return redirect(url_for('select_grade'))

    return render_template('create_flashcard.html', categories=categories)



# Route für das Löschen einer Karteikarte
@app.route('/delete_flashcard/<int:flashcard_id>', methods=['POST'])
def delete_flashcard(flashcard_id):
    user_id = session.get('user_id')
    if user_id is None:
        flash('Du musst eingeloggt sein, um eine Karteikarte zu löschen.', 'danger')
        return redirect(url_for('login'))
    
    db.delete_flashcard(flashcard_id, user_id)
    flash('Karteikarte erfolgreich gelöscht!', 'success')
    return redirect(url_for('view_flashcards'))

# Funktion, um die Datenbank zu initialisieren
def init_db_command():
    db.init_db()
    print("Datenbank erfolgreich initialisiert!")



@app.route('/mark_known/<int:flashcard_id>', methods=['POST'])
def mark_known(flashcard_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    db_con = get_db_con()
    db_con.execute('''
        UPDATE flashcards
        SET is_learned = 1
        WHERE id = ? AND user_id = ?
    ''', (flashcard_id, user_id))
    db_con.commit()
    return jsonify({'success': True})


@app.route('/mark_unknown/<int:flashcard_id>', methods=['POST'])
def mark_unknown(flashcard_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    db_con = get_db_con()
    db_con.execute('''
        UPDATE flashcards
        SET is_learned = 0
        WHERE id = ? AND user_id = ?
    ''', (flashcard_id, user_id))
    db_con.commit()
    return jsonify({'success': True})



from flask import session

@app.route('/start_test', methods=['GET'])
def start_test():
    user_id = session.get('user_id')
    if not user_id:
        flash('Du musst eingeloggt sein, um den Test zu starten.', 'danger')
        return redirect(url_for('login'))

    db_con = get_db_con()

    selected_category = session.get('selected_category')
    selected_grade = session.get('selected_grade')

    flashcards = db_con.execute('''
        SELECT id, category, question, answer
        FROM flashcards
        WHERE user_id = ? 
          AND category = ? AND grade_level = ?
        ORDER BY id
    ''', (user_id, selected_category, selected_grade)).fetchall()

    if not flashcards:
        flash('Keine unbeantworteten Karteikarten für die gewählten Filter gefunden.', 'warning')
        return redirect(url_for('view_flashcards'))
    session['test'] = {
        'flashcards': [dict(card) for card in flashcards],  # Convert rows to dicts
        'current_index': 0,
        'correct_answers': 0,
        'incorrect_answers': 0,
    }

    return redirect(url_for('test_mode'))


@app.route('/test_mode')
def test_mode():
    test_session = session.get('test')
    if not test_session or not test_session['flashcards']:
        flash('Keine aktive Testsitzung gefunden. Starte einen neuen Test.', 'danger')
        return redirect(url_for('start_test'))

    current_index = test_session['current_index']
    if current_index >= len(test_session['flashcards']):
        return render_template('test_mode.html', flashcard=[])

    flashcard = test_session['flashcards'][current_index]
    return render_template('test_mode.html', flashcard=flashcard)


@app.route('/submit_test_result', methods=['POST'])
def submit_test_result():
    test_session = session.get('test')
    if not test_session:
        return jsonify({'error': 'No active test session'}), 400

    data = request.json
    is_correct = data.get('is_correct')

    if is_correct:
        test_session['correct_answers'] += 1
    else:
        test_session['incorrect_answers'] += 1

    test_session['current_index'] += 1
    session['test'] = test_session  # Save updates

    if test_session['current_index'] >= len(test_session['flashcards']):
        db_con = get_db_con()
        db_con.execute('''
            INSERT INTO test_results (user_id, total_questions, correct_answers, incorrect_answers)
            VALUES (?, ?, ?, ?)
        ''', (
            session.get('user_id'),
            len(test_session['flashcards']),
            test_session['correct_answers'],
            test_session['incorrect_answers']
        ))
        db_con.commit()
        return jsonify({'message': 'Test completed'}), 200

    return jsonify({'success': True})

@app.route('/next_flashcard', methods=['GET'])
def next_flashcard():
    test_session = session.get('test')
    if not test_session:
        return redirect(url_for('start_test'))

    current_index = test_session['current_index']
    if current_index >= len(test_session['flashcards']):
        return jsonify({
            'message': 'Test completed',
            'correct_answers': test_session['correct_answers'],
            'incorrect_answers': test_session['incorrect_answers'],
            'total_questions': len(test_session['flashcards']),
        }), 200

    flashcard = test_session['flashcards'][current_index]
    return jsonify({'flashcard': flashcard})



@app.route('/profile')
def profile():
    # db.drop_tables()
    # db.init_db()
    user_id = session.get('user_id')
    if not user_id:
        flash('Du musst eingeloggt sein, um dein Profil zu sehen.', 'danger')
        return redirect(url_for('login'))

    db_con = get_db_con()
    user = db_con.execute('SELECT username FROM users WHERE id = ?', (user_id,)).fetchone()

    test_history = db_con.execute('''
        SELECT test_date, total_questions, correct_answers, incorrect_answers
        FROM test_results
        WHERE user_id = ?
        ORDER BY test_date DESC
    ''', (user_id,)).fetchall()

    test_stats = db_con.execute('''
        SELECT COUNT(*) AS total_tests,
               SUM(total_questions) AS total_questions,
               SUM(correct_answers) AS total_correct,
               SUM(incorrect_answers) AS total_incorrect
        FROM test_results
        WHERE user_id = ?
    ''', (user_id,)).fetchone()

    return render_template('profile.html', user=user, test_history=test_history, test_stats=test_stats)




if __name__ == '__main__':
    app.run(debug=True)
