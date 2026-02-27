import ensurepip
ensurepip.bootstrap()
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "h5py", "medpy", "SimpleITK", "tqdm", "ml-collections", "-q"])
print("Done installing packages")
