"""
Flask Application for BioDock Visualiser Webtool
    - Authors: Ramon Reilman, Stijn Vermeulen, Yamila Timmer

This Flask application handles the back-end for the webtool. It includes routes for
functionalities such as:
    - Submitting forms (with files in it)
    - Displaying images
    - Retrieving previous user-sessions of webtool (including files and imgs)

Usage:
    Run this script (run_app.py) to start up the Flask web application. 
    Access the webtool through the URL displayed in the terminal.

Commandline usage: 
    - python3 run_app.py
"""
import os
from flask import Flask, render_template, request, redirect, abort, send_file, url_for, session
from used_functions.functions_hist_page import clear_me, save_settings, load_settings, settings_dok_file, mol2_to_ligands
from used_functions.classes.lepro_class import LePro

app = Flask(__name__)
# sets max. file limit to be uploaded by the user
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# sets allowed file extensions for user uploads
app.config['UPLOAD_EXTENSIONS'] = ['.pdb', '.mol2']

@app.errorhandler(413)
def exceeds_capacity_limit(error):
    """
    Function to catch and handle the 413 errors
    :param error:
    :return: rendered own defined 413.html
    """
    return render_template('error_templates/413.html'), 413


@app.route('/', methods=['POST', 'GET'])
def webtool():
    """
    Handles GET and POST requests for the webtool page (index.html) 
    and form functionality. When a GET-request is received, it renders the
    index.html template. When a POST-request is received (so when a form is submitted), 
    it handles the form data. 

    Returns:
        - In case of a GET-request:
            Renders the index.html template
        - In case of a POST-request with invalid files:
            Aborts with a 400 error code
        - In case of a POST-request with valid files:
            Renders form_POST.html with submitted data 
            Saves a directory (with a user-specified name) with the uploaded files
    """
    if request.method == 'GET':
        # default response when a form is called, renders index.html
        return render_template("index.html", webtool_active=True, name_exists=False)

    # response when the submit button is clicked in index.html
    # packs the variables in dictionary 'kwargs'
    kwargs = {
        'dock_slider': request.form['dock_slider'],
        'RMSD_slider': request.form['RMSD_slider'],
        'name_file': request.form['name_file'],

    }

    # checks if the name already exists, if it does it returns the name_exists as true
    if kwargs['name_file'] in os.listdir('static/history'):
        # print(os.listdir("static/history"))
        return render_template("index.html", webtool_active=True, name_exists=True)

    # sets allowed upload file extensions to .pdb and .mol2, will give an 400 error
    # if user uploads file with other extension
    pdb_file = request.files['pdb_file']
    mol2_file = request.files['mol2_file']
    pdb_file_ext = os.path.splitext(pdb_file.filename)[1]
    mol2_file_ext = os.path.splitext(mol2_file.filename)[1]

    # checks if both files got uploaded, otherwise the input will be equal to ''
    if pdb_file.filename and mol2_file.filename != '':

        # checks if uploaded files have the correct extension, else returns an error
        if pdb_file_ext not in app.config['UPLOAD_EXTENSIONS'] \
        or mol2_file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(413)

        # checks the size of the mol2 file, returns an error of it exceeds the size limit
        mol2_file.seek(0, os.SEEK_END)
        mol2_length = mol2_file.tell()
        mol2_file.seek(0)
        if mol2_length > 3000: #TEST change this to the correct number
            abort(400)

        # creates directory with the name that the user chose for the session
        save_dir = os.path.join(app.root_path, "static", "history", kwargs['name_file'])
        os.makedirs(save_dir, exist_ok=True)

        # variables for the names of the files
        pdb_file_name = pdb_file.filename
        mol2_file_name = mol2_file.filename

        # saves both files in the newly created directory
        pdb_file.save(os.path.join(save_dir, pdb_file_name))
        mol2_file.save(os.path.join(save_dir, mol2_file_name))

        # creates json file and saves user-specified settings to it
        save_settings(save_dir, **kwargs)

        # creates instance for LePro-class
        lepro_instance = LePro(pdb_save_path = os.path.join(save_dir, pdb_file_name), name_file=kwargs['name_file'], new_save_path_dock = os.path.join("static/history/", kwargs['name_file'], "dock.in"))
        
        # runs run-method to activate LePro and moves output files to correct folder
        lepro_instance.run()

        # gives __str__ output with info about the running proces
        print(lepro_instance)
    
        # runs settings_dok_file-function which transfers the user input from kwargs dict to dock.in file
        settings_dok_file(lepro_instance.new_save_path_dock, kwargs['RMSD_slider'], kwargs['dock_slider'])

    # render the 'form_POST.html' with the variables collected from the form in index.html
    return render_template('form_POST.html', **kwargs)



@app.route("/template", methods=["POST", "GET"])
def template():
    """
    Displays the images and dok file created from the webtool or selected in history. The user 
    can download the files on this page.

    Returns:
        Renders the correct temp.html template
        In case of a POST-request:
            Downloads the file that matches the clicked button
    """

    # get the directory that was given in history
    project_name = request.args["project"]
    save_dir = os.path.join("static", "history", project_name)
    settings = load_settings(save_dir)

    # get the path to the static files
    img_path = f"static/history/{project_name}"
    imgs = []

    # define mol2 and pdb variables
    mol2_files = []
    pdb_file = ""

    # make the filenames accessible for looping
    static_path = os.walk(img_path)
    temp_img = []

    for (_dirpath, _dirnames, filenames) in static_path:

        for filename in filenames:

            if filename.endswith(".png"):
            # adds pictures to temp_img
                temp_img.append(filename)

                # make groups of 2 to display next to each other
                if len(temp_img) == 2:
                    imgs.append(temp_img)
                    temp_img = []

            # get the .dok file and make sure it is not displayed as a picture
            elif filename.endswith(".dok"):
                dok_file = filename

            elif filename == "ligands":
                with open(os.path.join("static", "history", project_name, filename), "rt") as ligands:
                    for line in ligands:
                        print(line)
                        line = line.replace("\n", "")
                        mol2_files.append(os.path.join("static", "history", project_name, str(line)))

            elif filename.endswith(".pdb"):
                if filename != "pro.pdb" and filename != "pro_protonated.pdb" and "plipfixed" not in filename:
                    pdb_file = os.path.join("static", "history", project_name, filename)

        # adds left-over image
        if temp_img:
            imgs.append(temp_img)


    if request.method == "POST":

        # check which kind of button is pressed
        if "Download_picture" in request.form:

            # get the wanted file
            image = request.form["Download_picture"]

            # get file path
            file_to_download = os.path.join(img_path, image)

            # get the system to download the file
            return send_file(file_to_download, as_attachment=True)

        if "file_download" in request.form:
            # get the wanted .dok file
            dok_file = request.form["file_download"]

            # get the path to the file
            file_to_download = os.path.join(img_path, dok_file)

            # make system download the file
            return send_file(file_to_download, as_attachment=True)

    return render_template("temp.html", history_active=True, imgs=imgs,
                           file_wanted=project_name, dok_file=dok_file, pdb_file=pdb_file, mol2_files=mol2_files,
                           RMSD_slider=settings["RMSD_slider"], dock_slider=settings["dock_slider"])


@app.route("/ourteam")
def our_team():
    """
    Renders the our_team.html template

    Returns:
        our_team.html template
    
    """
    return render_template("our_team.html", ourteam_active=True)


@app.route("/history", methods=["POST", "GET"])
def history():
    """
    handles the back end of the history page (history.html) and form request.
    When a GET-request is recieved it will render the normal history.html page.
    This page includes a table with past projects.
    When a POST-request is recieved it will redirect to the url of the temp.html route.
    
    Returns:
        - Incase of GET-request
            Renders the history.html template

        - Incase of POST-request
            redirects to the url of the temp.html with project name in url.
    
    """
    # Path of history folder and lists all dirs in this path
    path = "static/history"
    dir_list = os.listdir(path)

    # Render history page with the files in dir_list
    if request.method == "GET":
        return render_template("history.html", files=dir_list, history_active=True)

    if request.method == "POST":
        print(request.form.values())
        # Delete history
        user_input = request.form["user_input"]
        if user_input == "clear_me":
            print("Everything has been deleted")

            # uncomment to enable deleting
            # clear_me()
            return redirect("/")
        return redirect(url_for("template", project=user_input, **request.args))


@app.route("/about")
def about():
    """
    Renders the about.html template

    Returns:
        about.html template
    
    """
    return render_template("about.html", about_active=True)


if __name__ == "__main__":
    app.debug = True
    app.run()
