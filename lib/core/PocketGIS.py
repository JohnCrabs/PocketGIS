from osgeo import gdal
import netCDF4 as nc
import subprocess

import lib.core.fileFormats as file_formats
import lib.core.file_manipulation as file_manip


class PocketGIS:
    def __init__(self):
        self.gisFile = None

    def openFileGIS(self, path):
        suffix = file_manip.pathFileSuffix(path)
        if suffix in file_formats.NET_CDF:
            ds = nc.Dataset(path)
            print(ds)


if __name__ == "__main__":
    netCDFdat_path = '../../Data/S5P_OFFL_L1B_RA_BD1_20200601T102419_20200601T120549_13649_01_010000_20200601T134729.nc'
    pGIS = PocketGIS()
    pGIS.openFileGIS(netCDFdat_path)

    print(subprocess.Popen(['pip', 'show', 'numpy'], stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])


