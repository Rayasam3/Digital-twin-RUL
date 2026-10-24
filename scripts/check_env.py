import sys
import torch

print("Python  :", sys.version.split()[0])
print("PyTorch :", torch.__version__)
print("CUDA OK :", torch.cuda.is_available())

if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print("GPU     :", props.name)
    print("VRAM    : %.1f GB" % (props.total_memory / 1024**3))
    # quick sanity test: run a small calculation on the GPU
    x = torch.randn(1000, 1000, device="cuda")
    print("GPU test:", (x @ x).sum().item() != 0)
else:
    print("No GPU detected. Reinstall PyTorch with a CUDA build "
          "and update your NVIDIA driver.")