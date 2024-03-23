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
from flask import Flask, render_template, request, redirect, abort, send_file, url_for
from used_functions.functions_used import clear_me, save_settings, load_settings, \
    settings_dok_file, mol2_to_ligands, parse_config
from used_functions.classes.tool_classes import LePro, Ledock, Plip
from used_functions import merge_pdb_dok


app = Flask(__name__)

# sets allowed file extensions for user uploads
app.config['UPLOAD_EXTENSIONS'] = ['.pdb', '.mol2']

@app.errorhandler(412)
def precondition_failed(error):
    """
    Function to catch and handle the 412 errors

    :return: renders error.html with 412-specific args
    """
    print(error)
    return render_template('error.html', status_code=412, description='Precondition Failed',
                        message='Make sure that all required tools  (LePro, LeDock, PLIP) are \
                              installed in the virtual environment.'), 412


@app.errorhandler(413)
def payload_too_large(error):
    """
    Function to catch and handle the 413 errors

    :return: renders error.html with 413-specific args
    """
    print(error)
    return render_template('error.html', status_code=413, description='Payload Too Large',
                        message='Please submit a smaller MOL2 file.'), 413


@app.errorhandler(415)
def unsupported_media_type(error):
    """
    Function to catch and handle the 415 errors

    :return: renders error.html with 415-specific args
    """
    print(error)

    return render_template('error.html', status_code=415, description='Unsupported Media Type',
                        message='Make sure to upload only supported media types \
                            (.pdb and .mol2).'), 415


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
    img_path = config_path['paths']['img_path']
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
        # which is 415: Unsupported Media Type
        if pdb_file_ext not in app.config['UPLOAD_EXTENSIONS'] \
        or mol2_file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(415)

        # checks the size of the mol2 file, returns an error of it exceeds the size limit
        mol2_file.seek(0, os.SEEK_END)
        mol2_length = mol2_file.tell()
        mol2_file.seek(0)

        # raises error (413: Payload Too Large) if mol2 file is bigger than 3000 bytes
        if mol2_length > 3000:
            abort(413, 'Content Too Large', ' Please submit a smaller MOL2-file.')

        # creates directory with the name that the user chose for the session
        save_dir = os.path.join(img_path, kwargs['name_file'])
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
        lepro_instance = LePro(pdb_save_path = os.path.join(save_dir, pdb_file_name),
                               name_file=kwargs['name_file'], new_save_path_dock = \
                                os.path.join("static/history/", \
                                             kwargs['name_file'], "dock.in"))

        # raises error (412 Precondition Not Found) if LePro installation is not found
        if lepro_instance.lepro_path == '':
            abort(412)

        # runs run-method to activate LePro and moves output files to correct folder
        lepro_instance.run()

        # gives __str__ output with info about the running proces
        print(lepro_instance)

        # runs settings_dok_file-function which transfers the user input from kwargs
        # dict to dock.in file
        settings_dok_file(lepro_instance.new_save_path_dock, kwargs['RMSD_slider'], \
                          kwargs['dock_slider'])


        mol2_to_ligands(path=save_dir)
        mol2_for_dock = mol2_file_name.replace(".mol2", ".in")

        # creates instance for LeDock-class
        ledock_instance = Ledock(path=save_dir, file_name=mol2_for_dock)

        # raises error (412 Precondition Not Found) if LeDock installation is not found
        if ledock_instance.dock_path.stdout.strip() == '':
            abort(412)

        # runs run-method to activate LeDock
        ledock_instance.run()

        n_ligands = merge_pdb_dok.main(pdb_file=save_dir+"/pro.pdb", \
                            lig_file=save_dir+"/"+mol2_file_name.replace(".mol2", ".dok"))

        plip_instance = Plip(project_name=kwargs['name_file'], img_n=n_ligands)

        plip_instance.run()

        return redirect(url_for("template", project=kwargs["name_file"], **request.args))

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
    img_path = config_path['paths']['img_path']
    project_name = request.args["project"]
    save_dir = os.path.join(img_path, project_name)
    settings = load_settings(save_dir)

    # define mol2 and pdb variables
    mol2_file = ""
    pdb_file = ""

    # make the filenames accessible for looping
    static_path = os.walk(img_path + project_name)
    score_list = []
    img_list = []
    img_score_dict = {}

    
    for (_dirpath, _dirnames, filenames) in static_path:

        for filename in filenames:

            # adds all imgs to img_list
            if filename.endswith(".png"):
                img_list.append(filename)

            # get the .dok file and make sure it is not displayed as a picture
            elif filename.endswith(".dok"):
                dok_file = filename

            # looks in the ligands file for the mol2 file(s
            elif filename.endswith(".mol2"):
                mol2_file_name = filename
                mol2_file = os.path.join("static", "history", \
                            project_name, str(filename))

            # goes through a number of criteria to check if the .pdb file is not made by one 
            # of the functions of the website
            elif filename.endswith(".pdb"):
                if filename != "pro.pdb" and filename != "pro_protonated.pdb" and "plipfixed" not in filename:
                    pdb_file_name = filename
                    pdb_file = os.path.join("static", "history", project_name, filename)
            
    lig_dok_path =  f"static/history/{project_name}/{dok_file}"
    with open(lig_dok_path, encoding='utf-8') as lig_dok_file:

        # adds each line with 'Score' in it to score_list
        for line in lig_dok_file:
            if 'Score' in line:
                score = line.strip()
                score_list.append(score)

            # sorts the imgs alphabetically, so that the imgs will be displayed from
            # high 'ranking' to low
            sorted_imgs = sorted(img_list)
            print(sorted_imgs, score_list)
            # makes dict with img:score pairs
            for img, score in zip(sorted_imgs, score_list):
                img_score_dict[img] = score
        print(img_score_dict)

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
            file_to_download = os.path.join("static", "history", \
                            project_name, str(dok_file))
            
            # make system download the file
            return send_file(file_to_download, as_attachment=True)

    return render_template("temp.html", history_active=True, img_score_dict=img_score_dict,
                           file_wanted=project_name, dok_file=dok_file, pdb_file=pdb_file, \
                            mol2_file=mol2_file, pdb_file_name=pdb_file_name, \
                            mol2_file_name=mol2_file_name, 
                            RMSD_slider=settings["RMSD_slider"], \
                            dock_slider=settings["dock_slider"])


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
    img_path = config_path['paths']['img_path']
    dir_list = os.listdir(img_path)

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
            clear_me()

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
    # sets allowed file extensions for user uploads
    app.config['UPLOAD_EXTENSIONS'] = ['.pdb', '.mol2']

    config_path = parse_config()


    app.debug = True
    app.run()
