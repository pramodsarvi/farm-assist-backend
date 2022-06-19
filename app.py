import os
from fastapi import FastAPI
from fastapi import File, UploadFile, FastAPI

# UPLOAD_FOLDER = 'D:\\VSCODE\\project\\BACK\\'
# UPLOAD_FOLDER = os.getcwd()


app = FastAPI()
import shutil

# from flask_restful import Resource, Api
import datetime
from torch import device
from torch import load
from torch import max as torchmax
from torchvision import transforms
import os
import PIL.Image as Image

ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
import logging
import boto3
from botocore.exceptions import ClientError
import os
# AKIAT6M3J755ESRJNFML
# YI6+Vx7BctLHpkE+BDqzEuwM4pQu6UkEGmb1XYGe

def upload_file_s3(file_name):

    # s3 = boto3.resource('s3', use_ssl=False, verify=False)
    s3_client = boto3.client('s3',aws_access_key_id='AKIAT6M3J755ESRJNFML',aws_secret_access_key='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')
    # s3_client = boto3.client('s3',aws_access_key_id=os.environ['ACCESS_KEY'],aws_secret_access_key=os.environ['SECRET_KEY'])
    try:
        response = s3_client.upload_file(file_name, "farmassist", file_name)
    except Exception as e:
        logging.error(e)
        return False
    os.remove(file_name)
    return True

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/')
def hello_world():
    return '<h1>Hello World</h1>'

@app.post('/grape')
async def upload_file_grape(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        print(file.filename)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()
        
    pred_transforms = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    print("hit")
    class_names=['Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)','Grape___healthy']
	# check if the post request has the file part
    model_grape=load("model_grape.pt",map_location=device('cpu') )
    
    

    # if 'file' not in request.files:
    #     resp = {'message' : 'No file part in the request'}
    #     resp.status_code = 400
    #     return resp

    # file = request.files['file']
    # if file.filename == '':
    #     resp = {'message' : 'No file selected for uploading'}
    #     resp.status_code = 400
    #     return resp

    if file and allowed_file(file.filename):
        
        filename = file.filename
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("file_upload")
        # actual work
        pred=classify(model_grape,pred_transforms,filename,class_names)
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
            resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides : Mancozeb Ziram","path":newfile,"disease":"Black Rot","url":"https://farmassist.s3.ap-south-1.amazonaws.com/"+newfile}
        elif pred=="Grape___Esca_(Black_Measles)":
            resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides : Dormant sprays of lime,mancozeb and ziram","path":newfile,"disease":"Black Measles","url":"https://farmassist.s3.ap-south-1.amazonaws.com/"+newfile}
        elif pred=="Grape___Leaf_blight_(Isariopsis_Leaf_Spot)":
            resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides : Spraying of the grapevines at 3-4 leaf stage with fungicides like Bordeaux mixture at 0.8% or copper oxychloride at 025% or Carbendazim at 0.1% are effective against this disease","path":newfile,"disease":"Isariopsis Leaf Spot","url":"https://farmassist.s3.ap-south-1.amazonaws.com/"+newfile}
        else:
            resp = {'message' : 'File successfully uploaded',"pesticides":"","path":newfile,"disease":"Healthy","url":"https://farmassist.s3.ap-south-1.amazonaws.com/"+newfile}
        # resp.status_code = 201
        return resp
    else:
        resp = {'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'}
        # resp.status_code = 400
        return resp


# **********************************************************************************************************************************************************************************************************
@app.post('/tomato')
async def upload_file_tomato(file: UploadFile = File(...)):
    
    try:
        contents = await file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        print(file.filename)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()
        
    pred_transforms = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    class_names=['Tomato___Blight', 'Tomato___Leaf_Mold', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___healthy','Tomato_powdery_Mildew']
# # check if the post request has the file part
    model_grape=load("model_tomato_new.pt",map_location=device('cpu') )
    
    

    # if 'file' not in request.files:
    #     resp = {'message' : 'No file part in the request'}
    #     resp.status_code = 400
    #     return resp

    # file = request.files['file']
    # if file.filename == '':
    #     resp = {'message' : 'No file selected for uploading'}
    #     resp.status_code = 400
    #     return resp

    if file and allowed_file(file.filename):
        
        filename = file.filename
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("file_upload")
        # actual work
        pred=classify(model_grape,pred_transforms,filename,class_names)
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

        if pred==class_names[0]:
            resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides:Myclobutanil","disease":"Apple Scab"}
        elif pred==class_names[1]:
            resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides: Copper oxychloride(spraying with copper oxychloride at a concentration of 5-7g/L of water.)","disease":"Black Rot"}
        elif pred==class_names[2]:
            resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides:Chlorathalonil(Daconil),Mancozeb,Sulfur,Thiram,and Ziram","disease":"Cedar Apple Rust"}
        else:
            resp = {'message' : 'File successfully uploaded',"pesticides":""}

        return resp
    else:
        resp = {'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'}
        # resp.status_code = 400
    return resp



# /****************************************
# @app.post('/tomato')
# def upload_file_tomato():
#     pred_transforms = transforms.Compose([
#         transforms.RandomResizedCrop(224),
#         transforms.ToTensor(),
#         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
#     ])
#     print("hit")
#     class_names=['Tomato___Blight',
#  'Tomato___Leaf_Mold',
#  'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
#  'Tomato___healthy',
#  'Tomato_powdery_Mildew']
# 	# check if the post request has the file part
#     model_tomato=load("model_grape.pt",map_location=device('cpu') )
    
    

#     # if 'file' not in request.files:
#     #     resp = {'message' : 'No file part in the request'}
#     #     # resp.status_code = 400
#     #     return resp

#     # file = request.files['file']
#     # if file.filename == '':
#     #     resp = {'message' : 'No file selected for uploading'}
#     #     return {'message' : 'No file selected for uploading'}

#     if file and allowed_file(file.filename):
        
#         filename = file.filename
#         # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         print("file_upload")
#         # actual work
#         pred=classify(model_tomato,pred_transforms,filename,class_names)
#         # 
#         # save image with name
#         ct = datetime.datetime.now()
#         print("current time:-", ct)
        
#         # ts store timestamp of current time
#         ts = "".join(str(ct.timestamp()).split('.'))
#         print(ts)
#         print(pred)
#         os.rename(filename,pred+str(ts)+".jpg")
#         # send disease

#         if pred==class_names[0]:
#             resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides : Mancozeb ,Ziram"}
#         elif pred==class_names[1]:
#             resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides : Dormant sprays of Mancozeb and Ziram"}
#         elif pred==class_names[2]:
#             resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides : Spraying of the grapevines at 3-4 leaf stage with fungicides like Bordeaux mixture at 0.8% or copper oxychloride at 025% or Carbendazim at 0.1% are effective against this disease"}
#         else:
#             resp = {'message' : 'File successfully uploaded',"pesticides":""}
#         # resp = {'message' : 'File successfully uploaded'}
#         return resp
#     else:
#         resp = {'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'}
#         return resp
@app.post('/apple')
async def upload_file_apple(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        print(file.filename)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()

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
    model=load("model_apple10.pt",map_location=device('cpu') )
    
    

    # if 'file' not in request.files:
    #     resp = {'message' : 'No file part in the request'}
    #     # resp.status_code = 400
    #     return resp

    # file = request.files['file']
    # if file.filename == '':
    #     resp = {'message' : 'No file selected for uploading'}
    #     # resp.status_code = 400
    #     return resp

    if file and allowed_file(file.filename):
        
        filename = file.filename
        
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
            resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides:Myclobutanil","disease":"Apple Scab"}
        elif pred==class_names[1]:
            resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides: Copper oxychloride(spraying with copper oxychloride at a concentration of 5-7g/L of water.)","disease":"Black Rot"}
        elif pred==class_names[2]:
            resp = {'message' : 'File successfully uploaded',"pesticides":"Pesticides:Chlorathalonil(Daconil),Mancozeb,Sulfur,Thiram,and Ziram","disease":"Cedar Apple Rust"}
        else:
            resp = {'message' : 'File successfully uploaded',"pesticides":""}
        # resp = {'message' : 'File successfully uploaded'}
        # resp.status_code = 201
        return resp 
    else:
        resp = {'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'}
        # resp.status_code = 400
        return resp

def classify(model,image_transform,img_path,class_names):
    model=model.eval()
    image=Image.open(img_path)
    image=image_transform(image).float()
    image=image.unsqueeze(0)
    out=model(image)
    _,pred=torchmax(out.data,1)
    return class_names[pred.item()]




# uvicorn main:app --host 0.0.0.0 --port 5000
# torch==1.11.0+cpu
# torchvision==0.12.0+cpu
# torchaudio==0.11.0+cpu