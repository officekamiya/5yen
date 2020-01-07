# momme

## They are for HX711 on Raspberry Pi

pip install --upgrade -t ./site-packages/ RPi.GPIO

pip install --upgrade -t ./site-packages/ numpy

## They are for Kivy on Raspberry Pi

pip install --upgrade -t ./site-packages/ Cython

pip install --upgrade -t ./site-packages/ pillow

pip install --upgrade -t ./site-packages/ kivy

## It is Python Script for HX711

git submodule add https://github.com/tatobari/hx711py.git ./site-packages/hx711

## It is Japanese Font
git submodule add https://github.com/googlefonts/noto-cjk.git ./fonts/noto-cjk
