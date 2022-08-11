from flask import Flask, render_template, request

app = Flask(__name__)

user_history = {}

@app.route('/', methods=["GET"])
def hello_world():
    return render_template("index.html")

def log(age, canvote, prediction):
    found = user_history.get(request.remote_addr)
    if not found:
        user_history[request.remote_addr] = []

    user_history[request.remote_addr].append({"ip": request.remote_addr, "age": age, "canvote": canvote, "prediction": prediction})

@app.route("/predict", methods=["POST"])
def predict():
    age = request.form.get("age")
    can_vote = request.form.get("canvote") == "on"

    if age is None:
        return render_template("prediction.html", error="Age is required.")

    if can_vote is None:
        return render_template("prediction.html", error="canvote is required.")

    prediction = bool(can_vote) and 100 >= int(age) >= 18
    log(age, can_vote, prediction)

    return render_template("prediction.html", canvote=prediction)

@app.route("/history")
def history():
    records = user_history.get(request.remote_addr)
    if records is None:
        records = []
    return render_template("history.html", records=records)


if __name__ == '__main__':
    app.run()
