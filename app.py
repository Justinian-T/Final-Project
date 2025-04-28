import Flask, request, jsonify, pandas as pd

from datetime import datetime
app = Flask("My App")
df = pd.read_csv("5000 Sales Records.csv")
@app.route("/")
def hello():
    return "Hello World... Welcome to the Server"

@app.route("/name/<name>")
def getMyName(name):
    return "Your name is: {}".format(name)

@app.route("/totalrecords")
def getTotalRecords():
    total = len(df.index)
    return f"Total Records:{total}"

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)