import os
from pathlib import Path

ROOT_PATH = os.path.abspath(Path(__file__).parent.parent)
print("root_path", ROOT_PATH)
APP_PATH = os.path.join(ROOT_PATH, 'app')
MEDIA_PATH = os.path.join(APP_PATH, 'media')
IMAGES_PATH = os.path.join(MEDIA_PATH, 'images')
