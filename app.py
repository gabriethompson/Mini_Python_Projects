# Main Flask application
from flask import Flask, render_template
from database import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
from flask import Flask, render_template, request, jsonify
from database import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Category pages
@app.route('/<category>')
def category_page(category):
    category_names = {"skills": "Skills Development", "psyche": "Psyche", "health": "Health"}
    if category not in category_names:
        return "You need jesus", 404
    return render_template('category.html', category_name=category_names[category], category_id=category)

# Update task completion in the database
@app.route('/update_task', methods=['POST'])
def update_task():
    data = request.get_json()
    category_id = data['category_id']
    day = data['day']

    task = Task.query.filter_by(category=category_id, day=day).first()
    if task:
        task.completed = not task.completed  # Toggle completion status
    else:
        task = Task(category=category_id, day=day, completed=True)
        db.session.add(task)

    db.session.commit()
    return jsonify(success=True)

@app.route('/get_task_status', methods=['GET'])
def get_task_status():
    category_id = request.args.get('category_id')
    day = request.args.get('day')

    task = Task.query.filter_by(category=category_id, day=day).first()
    return jsonify({"completed": task.completed if task else False})

if __name__ == '__main__':
    app.run(debug=True)