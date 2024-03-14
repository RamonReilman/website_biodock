import os
from flask import Flask, render_template, request, redirect, send_file
from used_functions.functions_hist_page import clear_me
app = Flask(__name__)

@app.route("/")
def webtool():
    return render_template("index.html", webtool_active=True)

@app.route("/template", methods=["POST", "GET"])
def template():
    file_wanted = "4zel.pdb"
    foto_path = f"static/history/{file_wanted}"
    fotos = []
    w=os.walk(foto_path)
    temp_foto = []
    for index, (dirpath, dirnames, filenames) in enumerate(w):
        for filename in filenames:
            if ".dok" in filename:
                dok_file = filename
            else:
                temp_foto.append(filename)
                if len(temp_foto) == 2:
                    fotos.append(temp_foto)
                    temp_foto = []
        if len(filenames) % 2 == 0:
            if ".dok" not in filenames[-1]:
                fotos.append([filenames[-1]])
            else:
                fotos.append([filenames[-2]])
    # print(fotos)
    if request.method == "POST":
        if "Download_picture" in request.form:
            image = request.form["Download_picture"]
            file_to_download = os.path.join(foto_path, image)
            return send_file(file_to_download, as_attachment=True)
            # return send_from_directory(f"{foto_path}", path)
        elif "file_download" in request.form:
            dok_file = request.form["file_download"]
            file_to_download = os.path.join(foto_path, dok_file)
            return send_file(file_to_download, as_attachment=True)
    return render_template("history/4zel.pdb/temp.html", webtool_active=True, fotos=fotos, file_wanted=file_wanted, dok_file=dok_file)

@app.route("/ourteam")
def our_team():
    return render_template("our_team.html", ourteam_active=True)

@app.route("/history", methods=["POST", "GET"])
def history():
    path = "templates/history"
    dir_list = os.listdir(path)

    if request.method == "GET":
        return render_template("history.html", files=dir_list, history_active=True)

    elif request.method == "POST":
        file_wanted = list(request.form.keys())
        file_wanted = str(file_wanted).replace("[", "").replace("]", "").replace("'", "")

        if file_wanted == "clear_me":
            print("Everything has been deleted")

            # uncomment to enable deleting
            # clear_me()
            return redirect("/")

        else:
            return render_template(f"history/{file_wanted}/temp.html")

@app.route("/about")
def about():
    return render_template("about.html", about_active=True)

if __name__ == "__main__":
    app.debug = True
    app.run()
