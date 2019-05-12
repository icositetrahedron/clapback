# clapback

## Install Requirements

Run

```
brew install portaudio
pip3 install -r requirements.txt
```

## Optional Calibration

This tool uses p2fa https://github.com/jaekookang/p2fa_py3 for calibration. A pre-made file is included in case installing the requirements is too complex for the user; this may impact effectiveness due to differences in speech and environment.

Download HTK-3.4.1 (NOT 3.5) from http://htk.eng.cam.ac.uk/. Registration is required.

Uncompress the package, and move the resulting htk directory into the clapback folder. 

cd into the htk directory. 

Run the following in the command line:

```
export CPPFLAGS=-UPHNALG
./configure --disable-hlmtools --disable-hslab
make clean    # necessary if you're not starting from scratch
make -j4 all
sudo make -j4 install
```

## Running

```
python3 clapback.py
```
