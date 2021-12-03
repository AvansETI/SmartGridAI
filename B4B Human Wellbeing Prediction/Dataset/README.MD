# ETL Notes
The source datasets can be found at https://github.com/IoTsec/Room-Climate-Datasets \
Download those datasets and put them alongside the notebooks, the file structure should look as follows.

+ Dataset
    + datasets-location_A
    + datasets-location_B
    + datasets-location_C

For the updated pythermalcomfort package you have to install the following package.
````
pip install https://github.com/maartendonkersloot/pythermalcomfort/archive/master.zip
````
If you get the following error.
````
ImportError: Numba needs NumPy 1.20 or less
````
Do the following or your equivalent and restart your kernel.
````
conda install numpy<1.20 
````