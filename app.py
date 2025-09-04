import flask
from flask import Flask, jsonify, request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory')
def inventory():
    
    return render_template('inventory.html')

@app.route('/contact')
def contact():
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)