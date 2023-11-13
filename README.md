# Campfire
A simple GUI wrapper for ChatGPT text-to-speech API functionality.

## Build Instructions
Campfire can be built and run on macOS in two distinct ways: either directly via Python or by creating a standalone macOS application. The python build should also work on Linux.

### Option 1: macOS Application Build
1. Clone the repository to your local machine and `cd` into it:
```bash
git clone git@github.com:j-hurwitz/campfire.git
cd campfire
```
2. Execute the build script to create the `.app`:
```bash
chmod +x macos-build.sh
./macos-build.sh
```
3. Optionally, place the `.app` inside your Applications folder.

### Option 2: Python Build
1. Clone the repository to your local machine and `cd` into it:
```bash
git clone git@github.com:j-hurwitz/campfire.git
cd campfire
```
2. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```
3. Run the main python script:
```bash
python campfire.py
```