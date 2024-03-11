from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def webtool():
    return render_template("index.html")

@app.route("/ourteam")
def our_team():
    return render_template("our_team.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
