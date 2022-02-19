import rasterio
import lib.core.common.file_manipulation as file_manip

import earthpy.plot as ep

MAIN_PATH = file_manip.PATH_DOCUMENTS + '/PocketGIS'
TEST_IMG_NDVI_SHOW = MAIN_PATH + '\\S02L1C\\S02L1C_B1_NDVI_S20210101E20210108_WGS84_LATS37c9E38c1_LONS23c6E23c8_W1692H2271.tiff'


def viewIMG(imgPath):
    img = rasterio.open(imgPath).read(1)
    ep.plot_bands(img, title=file_manip.pathFileName(TEST_IMG_NDVI_SHOW), cmap="RdYlGn", cols=1, vmin=-1, vmax=1)


if __name__ == "__main__":
    viewIMG(TEST_IMG_NDVI_SHOW)
