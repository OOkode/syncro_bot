from flask import Flask,request
app = Flask(__name__)

@app.route('/AAFVAZ71-YSUXBcct1wBQuYryHO-1BXXsDg')
def receive_updates():
    return 'Hello, World!'