
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory groceries list (will reset when server restarts)
groceries = []

@app.route('/')
def index():
    return render_template('index.html', groceries=groceries)

@app.route('/add', methods=['POST'])
def add():
    grocery = request.form.get('grocery')
    if grocery:
        groceries.append({'grocery': grocery, 'done': False})
    return redirect(url_for('index'))

@app.route('/complete/<int:grocery_id>')
def complete(grocery_id):
    if 0 <= grocery_id < len(groceries):
        groceries[grocery_id]['done'] = not groceries[grocery_id]['done']
    return redirect(url_for('index'))

@app.route('/delete/<int:grocery_id>')
def delete(grocery_id):
    if 0 <= grocery_id < len(groceries):
        groceries.pop(grocery_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

