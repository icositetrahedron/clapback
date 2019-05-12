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

Basic usage is:

```
python3 clapback.py
```

There are the following options:
-c: Record the calibration file.
-d: Use the default calibration file. This is only necessary if you have successfully recorded a calibration file which you wish to override; otherwise, the default calibration file is used automatically.
-l N: Set the recording time for N seconds. This is how long the script will run, listening for you and clapping.

Example:

```
python3 clapback.py -l 20 -c
```

This first makes you record the calibration file, then listens for 20 seconds and claps as you speak.
