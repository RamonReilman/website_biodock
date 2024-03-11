from flask import Flask, render_template, request
import os
app = Flask(__name__)

@app.route("/")
def webtool():
    return render_template("index.html", webtool_active=True)

@app.route("/ourteam")
def our_team():
    return render_template("our_team.html", ourteam_active=True)

@app.route("/history", methods=["POST", "GET"])
def history():
    if request.method == "GET":
        path = "templates/history"
        dir_list = os.listdir(path)
        return render_template("history.html", files=dir_list)
    
    elif request.method == "POST":
        file_wanted = list(request.form.keys())
        file_wanted = str(file_wanted).replace("[", "").replace("]", "").replace("'", "")
        return render_template(f"history/{file_wanted}/temp.html")

@app.route("/about")
def about():
    return render_template("about.html", about_active=True)

if __name__ == "__main__":
    app.debug = True
    app.run()
