import os
from flask import Flask, render_template, request, redirect
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
        # and checks if files are within file limit (turned off while in development)
        # app.config['MAX_CONTENT_LENGTH'] = 1024
        pdb_file = request.files['pdb_file']
        mol2_file = request.files['mol2_file']
        if pdb_file.filename and mol2_file.filename != '':

            # creates directory with the name that the user chose for the session
            save_dir = os.path.join("templates", "history", kwargs['name_file'])
            os.makedirs(save_dir, exist_ok=True)

            # saves both files in the newly created directory
            pdb_file.save(os.path.join(save_dir, pdb_file.filename))
            mol2_file.save(os.path.join(save_dir, mol2_file.filename))

        # render the 'form_POST.html' with the variables collected from the form in index.html
        return render_template('form_POST.html', **kwargs)

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
