import os
from app import app
import shutil
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import datetime
import torch
from torchvision import transforms
import os
import PIL.Image as Image

ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_file_s3(file_name):

    # If S3 object_name was not specified, use file_name


    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, "farmassist", file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

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
        pred=classify(model,pred_transforms,filename,class_names)
        # save image with name
        ct = datetime.datetime.now()
        print("current time:-", ct)
        
        # ts store timestamp of current time
        ts = "".join(str(ct.timestamp()).split('.'))
        print(ts)
        print(pred)
        newfile=str(ts)+".jpg"
        os.rename(filename,newfile)
        upload_file_s3(newfile)
        print("uploaded to s3")
        print("https://farmassist.s3.ap-south-1.amazonaws.com/"+newfile)

        # shutil.copy(newfile,'D:\\VSCODE\\project\\front\\upload_img\\src\\')
        # send disease
        # in response

        if pred=="Grape___Black_rot":                                                                                                                                              
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"Pesticides : Mancozeb Ziram","path":newfile,"disease":"Black Rot","url":"https://farmassist.s3.ap-south-1.amazonaws.com/"+newfile})
        elif pred=="Grape___Esca_(Black_Measles)":
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"Pesticides : Dormant sprays of lime,mancozeb and ziram","path":newfile,"disease":"Black Measles","url":"https://farmassist.s3.ap-south-1.amazonaws.com/"+newfile})
        elif pred=="Grape___Leaf_blight_(Isariopsis_Leaf_Spot)":
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"Pesticides : Spraying of the grapevines at 3-4 leaf stage with fungicides like Bordeaux mixture at 0.8% or copper oxychloride at 025% or Carbendazim at 0.1% are effective against this disease","path":newfile,"disease":"Isariopsis Leaf Spot","url":"https://farmassist.s3.ap-south-1.amazonaws.com/"+newfile})
        else:
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"","path":newfile,"disease":"Healthy","url":"https://farmassist.s3.ap-south-1.amazonaws.com/"+newfile})
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
    class_names=['Tomato___Blight',
 'Tomato___Leaf_Mold',
 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato___healthy',
 'Tomato_powdery_Mildew']
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
        pred=classify(model,pred_transforms,filename,class_names)
        # 
        # save image with name
        ct = datetime.datetime.now()
        print("current time:-", ct)
        
        # ts store timestamp of current time
        ts = "".join(str(ct.timestamp()).split('.'))
        print(ts)
        print(pred)
        os.rename(filename,pred+str(ts)+".jpg")
        # send disease

        if pred==class_names[0]:
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"Pesticides : Mancozeb ,Ziram"})
        elif pred==class_names[1]:
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"Pesticides : Dormant sprays of Mancozeb and Ziram"})
        elif pred==class_names[2]:
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"Pesticides : Spraying of the grapevines at 3-4 leaf stage with fungicides like Bordeaux mixture at 0.8% or copper oxychloride at 025% or Carbendazim at 0.1% are effective against this disease"})
        else:
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":""})
        # resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp
@app.route('/apple', methods=['POST'])
def upload_file_apple():
    pred_transforms = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    print("hit")
    class_names=['Apple___Apple_scab',
 'Apple___Black_rot',
 'Apple___Cedar_apple_rust',
 'Apple___healthy']
	# check if the post request has the file part
    model=torch.load("model_apple10.pt")
    
    

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
        pred=classify(model,pred_transforms,filename,class_names)
        ct = datetime.datetime.now()
        print("current time:-", ct)
        
        # ts store timestamp of current time
        ts = "".join(str(ct.timestamp()).split('.'))
        print(ts)
        print(pred)
        os.rename(filename,pred+str(ts)+".jpg")
        # send disease

        if pred==class_names[0]:
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"Pesticides:Myclobutanil","disease":"Apple Scab"})
        elif pred==class_names[1]:
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"Pesticides: Copper oxychloride(spraying with copper oxychloride at a concentration of 5-7g/L of water.)","disease":"Black Rot"})
        elif pred==class_names[2]:
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":"Pesticides:Chlorathalonil(Daconil),Mancozeb,Sulfur,Thiram,and Ziram","disease":"Cedar Apple Rust"})
        else:
            resp = jsonify({'message' : 'File successfully uploaded',"pesticides":""})
        # resp = jsonify({'message' : 'File successfully uploaded'})
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
        image = image.to("cpu")
        image=image.unsqueeze(0)
        out=model(image)
        _,pred=torch.max(out.data,1)
        return class_names[pred.item()]
    app.run(host='0.0.0.0', port=5000)
    




# torch==1.11.0+cpu
# torchvision==0.12.0+cpu
# torchaudio==0.11.0+cpu