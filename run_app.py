from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def webtool():
    return render_template("index.html", webtool_active=True)

@app.route("/ourteam")
def our_team():
    return render_template("our_team.html", ourteam_active=True)

@app.route("/history")
def history():
    return render_template("history.html", history_active=True)

@app.route("/about")
def about():
    return render_template("about.html", about_active=True)

if __name__ == "__main__":
    app.debug = True
    app.run()
