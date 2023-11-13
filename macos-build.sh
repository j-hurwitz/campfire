pip install -r requirements.txt
pip install pyinstaller

pyinstaller --add-data "resources/campfire.png:." campfire.py

APP_NAME="Campfire"
APP_DIR="${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"

mkdir -p "${CONTENTS_DIR}/MacOS"
mkdir -p "${CONTENTS_DIR}/Frameworks"
mkdir -p "${CONTENTS_DIR}/Resources"

cp Info.plist "${CONTENTS_DIR}/"
cp resources/app_icon.icns "${CONTENTS_DIR}/Resources"
cp dist/campfire/campfire "${CONTENTS_DIR}/MacOS"
cp -r dist/campfire/_internal/* "${CONTENTS_DIR}/Frameworks"






