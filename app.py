from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database/college_data.db'
PER_PAGE = 10  # 每页显示的结果数

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        major = request.form.get('major')
        school = request.form.get('school')
        min_score = request.form.get('min_score')
        max_score = request.form.get('max_score')
        min_rank = request.form.get('min_rank')
        max_rank = request.form.get('max_rank')

        query_params = {
            'major': major,
            'school': school,
            'min_score': min_score,
            'max_score': max_score,
            'min_rank': min_rank,
            'max_rank': max_rank
        }
        
        return redirect(url_for('results', **query_params))
    
    return render_template('index.html')

@app.route('/results')
def results():
    major = request.args.get('major')
    school = request.args.get('school')
    min_score = request.args.get('min_score')
    max_score = request.args.get('max_score')
    min_rank = request.args.get('min_rank')
    max_rank = request.args.get('max_rank')
    page = request.args.get('page', 1, type=int)

    query = "SELECT major, school, quota, score, rank FROM admissions WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM admissions WHERE 1=1"
    params = []

    if major:
        query += " AND major LIKE ?"
        count_query += " AND major LIKE ?"
        params.append('%' + major + '%')
    if school:
        query += " AND school LIKE ?"
        count_query += " AND school LIKE ?"
        params.append('%' + school + '%')
    if min_score:
        query += " AND score >= ?"
        count_query += " AND score >= ?"
        params.append(min_score)
    if max_score:
        query += " AND score <= ?"
        count_query += " AND score <= ?"
        params.append(max_score)
    if min_rank:
        query += " AND rank >= ?"
        count_query += " AND rank >= ?"
        params.append(min_rank)
    if max_rank:
        query += " AND rank <= ?"
        count_query += " AND rank <= ?"
        params.append(max_rank)

    # 获取总数
    cur = get_db().execute(count_query, params)
    total_results = cur.fetchone()[0]
    cur.close()

    query += " LIMIT ? OFFSET ?"
    params.extend([PER_PAGE, (page - 1) * PER_PAGE])

    cur = get_db().execute(query, params)
    results = cur.fetchall()
    cur.close()

    total_pages = (total_results + PER_PAGE - 1) // PER_PAGE

    return render_template('results.html', results=results, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
