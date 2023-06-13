#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import pipeline
from PIL import Image
import numpy as np
import shutil
import cv2
#import glob
#from pathlib import Path


FOLDER_VALIDATION_MASK   = "C:/Users/Utilisateur/PROJET8/input/P8_Cityscapes_gtFine_trainvaltest/gtFine"


app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png'])#, 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('Image non choisie')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('nom image: ' + filename)
        
        #########################RECHERCHE DU MASQUE REEL 30 classes ############################################
        name_mask_real_deduite = filename.replace('leftImg8bit', "gtFine_color")
        #print(name_mask_real)
        
        for root, dirs, files in os.walk(FOLDER_VALIDATION_MASK):
            for real_mask_input in files:
                if real_mask_input == name_mask_real_deduite:
                    print("boucle file",real_mask_input)
                    print("boucle dirs",dirs)
                    print("boucle root",root)
                    root = root.replace(os.path.sep, "/")
                    print("boucle root",root)
                    mask_real_path=root+'/'+real_mask_input
                    print("chemin complet",mask_real_path)
                    
                    #Copie du masque prédit dans le dossier static
                    shutil.copy(mask_real_path, 'static/uploads/')
                    
                    #mask_real_path.save('static/uploads/mask_real_image.png')
                    #mask_real= cv2.imread(mask_real_path)
                    
        
        ######################### FIN RECHERCHE DU MASQUE REEL 30 classes ########################################
        
        ######################### RECHERCHE DU MASQUE REEL 8 cats ############################################
            
        name_mask8_real_deduite = filename.replace('leftImg8bit', "gtFine_labelIds")
        #print(name_mask_real)
        
        for root, dirs, files in os.walk(FOLDER_VALIDATION_MASK):
            for real_mask8_input in files:
                if real_mask8_input == name_mask8_real_deduite:
                    print("boucle file",real_mask8_input)
                    print("boucle dirs",dirs)
                    print("boucle root",root)
                    root = root.replace(os.path.sep, "/")
                    print("boucle root",root)
                    mask8_real_path=root+'/'+real_mask8_input
                    print("chemin complet",mask8_real_path)
                    
                    #Copie du masque prédit dans le dossier static
                    shutil.copy(mask8_real_path, 'static/uploads/')
                    
                    #Colorisation du masque 8 cats
                    mask8_test = mask8_real_path
                    mask8_test_array = cv2.imread(mask8_test)
                    mask8_test_array_color=cv2.cvtColor(mask8_test_array, cv2.COLOR_BGR2GRAY) 
                    mask8_test_array_color = Image.fromarray((mask8_test_array_color * 8).astype(np.uint8))
                    mask8_test_array_color.save('static/uploads/mask8_image.png')
                    name_mask8_real_deduite = 'mask8_image.png'
                    
            
            
        ######################### FIN RECHERCHE DU MASQUE REEL 8 cats ########################################  
        
        #########################PREDICTION DU MASQUE################################################
        #image ="C:/Users/Utilisateur/PROJET8/input/P8_Cityscapes_leftImg8bit_trainvaltest/leftImg8bit/val/munster/munster_000034_000019_leftImg8bit.png"
        image='C:/Users/Utilisateur/PROJET8/static/uploads/' + filename
        #print(image)
        mask_t=pipeline.affichage_model_result(image)
        init_img = Image.fromarray((mask_t * 255).astype(np.uint8))
        init_img.save('static/uploads/mask_image.png')
        mask_filename = 'mask_image.png'
        print('nom mask: ' + mask_filename)

        
        #flash('Voici la vue prise par la voiture, le masque de segmentation original et le masque de ségmentation prédit associé')
        flash(filename)
        print(filename)
        print(name_mask_real_deduite)
        print(mask_filename)
        return render_template('index.html', filename=filename, name_mask_real_deduite=name_mask_real_deduite, name_mask8_real_deduite=name_mask8_real_deduite,mask_filename=mask_filename)
        #########################FINPREDICTION DU MASQUE################################################
    
    else:
        flash('Le type autorisé est png')
        return redirect(request.url)
    
    
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/display/<name_mask_real_deduite>')
def display_real_mask(name_mask_real_deduite):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + name_mask_real_deduite), code=301)

@app.route('/display/<name_mask8_real_deduite>')
def display_real_mask8(name_mask8_real_deduite):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + name_mask8_real_deduite), code=301)

@app.route('/display/<mask_filename>')
def display_mask(mask_filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + mask_filename), code=301)

if __name__ == "__main__":
    app.run()