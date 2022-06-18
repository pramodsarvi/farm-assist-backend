
from main import app
import torch 
import PIL.Image as Image
from waitress import serve
if __name__ == '__main__':
    def classify(model,image_transform,img_path,class_names):
        model=model.eval()
        image=Image.open(img_path)
        image=image_transform(image).float()
        image = image.to("cpu")
        image=image.unsqueeze(0)
        out=model(image)
        _,pred=torch.max(out.data,1)
        return class_names[pred.item()]
    
    serve(app, host="0.0.0.0", port=5000)
    # app.run()