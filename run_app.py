import os
from flask import Flask, render_template, request, redirect, abort, send_file, url_for
from used_functions.functions_hist_page import clear_me

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def webtool():
    if request.method == 'GET':
        # default response when a form is called, renders index.html
        return render_template("index.html", webtool_active=True)

    elif request.method == 'POST':
        # response when the submit button is clicked in index.html
        # packs the variables in dictionary 'kwargs'
        kwargs = {
            'dock_slider': request.form['dock_slider'],
            'RMSD_slider': request.form['RMSD_slider'],
            'name_file': request.form['name_file'],
        }

        # checks if both files (pdb and mol2) have been given by user
        # and checks if files are within file limit
        app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
        # sets allowed upload file extensions to .pdb and .mol2, will give an 400 error 
        # if user uploads file with other extension
        app.config['UPLOAD_EXTENSIONS'] = ['.pdb', '.mol2']
        pdb_file = request.files['pdb_file']
        mol2_file = request.files['mol2_file']
        pdb_file_ext = os.path.splitext(pdb_file.filename)[1]
        mol2_file_ext = os.path.splitext(mol2_file.filename)[1]
        if pdb_file_ext not in app.config['UPLOAD_EXTENSIONS'] or mol2_file_ext not in app.config:
            abort(400)


        if pdb_file.filename and mol2_file.filename != '':

            # creates directory with the name that the user chose for the session
            save_dir = os.path.join("templates", "history", kwargs['name_file'])
            os.makedirs(save_dir, exist_ok=True)

            # saves both files in the newly created directory
            pdb_file.save(os.path.join(save_dir, pdb_file.filename))
            mol2_file.save(os.path.join(save_dir, mol2_file.filename))

        # render the 'form_POST.html' with the variables collected from the form in index.html
        return render_template('form_POST.html', **kwargs)

@app.route("/template", methods=["POST", "GET"])
def template():
    project_name = request.args["project"]
    print(project_name)
    foto_path = f"static/history/{project_name}"
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
    return render_template("history/4zel.pdb/temp.html", history_active=True, fotos=fotos, file_wanted=project_name, dok_file=dok_file)

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
            # send wanted file to template url
            return redirect(url_for("template", project=file_wanted, **request.args))

@app.route("/about")
def about():
    return render_template("about.html", about_active=True)

if __name__ == "__main__":
    app.debug = True
    app.run()
