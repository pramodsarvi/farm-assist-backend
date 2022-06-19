import torch
model=torch.load('model_tomato_new.pt',map_location=torch.device('cpu') )
# model=torch.nn.Module()
# model.load_state_dict(torch.load('model_tomato_new.pt'))
print(model)