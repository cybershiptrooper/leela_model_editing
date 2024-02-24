import torch
from onnx2torch import convert

path="nets/512_filters_model.onnx"
torch_model = convert(path)
torch.save(torch_model, 'nets/512_torch.pt')