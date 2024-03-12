import os
from flask import Flask, render_template, request, redirect
from used_functions.functions_hist_page import clear_me
app = Flask(__name__)

@app.route("/")
def webtool():
    return render_template("index.html", webtool_active=True)

@app.route("/template")
def template():
    file_wanted = "4zel.pdb"
    foto_path = f"static/history/{file_wanted}"
    fotos = []
    w=os.walk(foto_path)
    temp_foto = []
    for index, (dirpath, dirnames, filenames) in enumerate(w):
        for filename in filenames:
            temp_foto.append(filename)
            if len(temp_foto) == 2:
                fotos.append(temp_foto)
                temp_foto = []
        if len(filenames) % 2 == 1:
            fotos.append([filenames[-1]])
    print(fotos)
    # if request.form['file_download'] == "Download":
    #     return redirect('../../../static/history/{{ fileName }}/PRO_PROTEIN_PeptideChain1.png')
    return render_template("history/4zel.pdb/temp.html", webtool_active=True, fotos=fotos, file_wanted=file_wanted)

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
