from flask import Flask, render_template, request
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
            'pdb_file': request.form['pdb_file'],
            'mol2_file': request.form['mol2_file'],
            'dock_slider': request.form['dock_slider'],
            'RMSD_slider': request.form['RMSD_slider'],
            'name_file': request.form['name_file'],
        }
        # render the 'form_POST.html' with the variables collected from the form in index.html
        return render_template('form_POST.html', **kwargs)

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
