# clapback

## Install Requirements

Run

```
brew install portaudio
pip3 install -r requirements.txt
```

## Optional Calibration

Calibration is optional but strongly recommended. Calibration sets threshholds for triggering clapping, based on the user's speech and environment. However, in the case that installation of calibration requirements is not possible, this section may be skipped.

This tool uses p2fa https://github.com/jaekookang/p2fa_py3for calibration; the files are already included.

### Calibration Requirement Installation

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
1. -c: Record the calibration file.
2. -d: Use the default calibration file. This is only necessary if you have successfully recorded a calibration file which you wish to override; otherwise, the default calibration file is used automatically.
3. -l N: Set the recording time for N seconds. This is how long the script will run, listening for you and clapping.
4. -o N: Set the clapping threshhold to N dBFS, where N is a float. The higher a number, the louder you will need to talk for the program to clap for you. You may wish to use this if calibration was not possible. The default threshold is about -16.

Example:

```
python3 clapback.py -l 20 -c
```

This first makes you record the calibration file, then listens for 20 seconds and claps as you speak.
