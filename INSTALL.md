# Instalar gi (pygobject)
ln -s /usr/lib/python3/dist-packages/gi <virtualenv>/lib/python3.5/site-packages/

pip install numpy
pip install netCDF4
pip install scipy
pip install matplotlib
pip install GDAL
pip install h5py
pip install cairocffi
pip install pyproj

# basemap
https://matplotlib.org/basemap/users/installing.html

# cairo
git clone git@github.com:pygobject/pycairo.git
cd pycauro
python setup.py install

# pyart (clonar, instalar y borrar)
git clone https://github.com/ARM-DOE/pyart.git
cd pyart
python setup.py install

# wradlib (clonar, instalar y borrar)
git clone git@github.com:wradlib/wradlib.git
cd wradlib/
python setup.py install
