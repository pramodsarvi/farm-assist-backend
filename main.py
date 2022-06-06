import os
from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
#run

import torch
from torchvision import transforms
import matplotlib.pyplot as plt
import os
import PIL.Image as Image

plt.ion()   # interactive mode
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/grape', methods=['POST'])
def upload_file():
    pred_transforms = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    print("hit")
    class_names=['Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)','Grape___healthy']
	# check if the post request has the file part
    model=torch.load("model_grape.pt")
    
    

    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    if file and allowed_file(file.filename):
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("file_upload")
        # actual work
        print(classify(model,pred_transforms,'4fdd1c1a-33fb-4409-8fbf-40f416abfde9___FAM_B.Rot 3272.JPG',class_names))
        # 

        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

@app.route('/tomato', methods=['POST'])
def upload_file_tomato():
    pred_transforms = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    print("hit")
    class_names=['Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)','Grape___healthy']
	# check if the post request has the file part
    model=torch.load("model_grape.pt")
    
    

    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    if file and allowed_file(file.filename):
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("file_upload")
        # actual work
        print(classify(model,pred_transforms,'4fdd1c1a-33fb-4409-8fbf-40f416abfde9___FAM_B.Rot 3272.JPG',class_names))
        # 

        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


if __name__ == "__main__":

    def classify(model,image_transform,img_path,class_names):
        model=model.eval()
        image=Image.open(img_path)
        image=image_transform(image).float()
        image = image.to("cuda")
        image=image.unsqueeze(0)
        out=model(image)
        _,pred=torch.max(out.data,1)
        print(class_names[pred.item()])
    app.run()