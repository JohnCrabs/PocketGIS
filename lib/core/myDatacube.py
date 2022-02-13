import rasterio
import lib.core.EvaluationScripts as evalScript
import lib.core.file_manipulation as file_manip

import earthpy.plot as ep

MAIN_PATH = file_manip.PATH_DOCUMENTS + '/PocketGIS'
TEST_IMG_NDVI_SHOW = MAIN_PATH + '\\S02L1C\\S02L1C_B1_NDVI_S20200108E20200115_WGS84_LONS23c61E23c66_LATS37c93E37c98.tif'

_DKEY_SATELLITE = 'satellite'
_DKEY_BANDS = 'bands'
_DKEY_DATA_TYPE = 'data-type'
_DKEY_DATE_START = 'date-start'
_DKEY_DATE_END = 'date-end'
_DKEY_CRS = 'crs'
_DKEY_LONGITUDE_MIN = 'longitude-min'
_DKEY_LONGITUDE_MAX = 'longitude-max'
_DKEY_LATITUDE_MIN = 'latitude-min'
_DKEY_LATITUDE_MAX = 'latitude-max'
_DKEY_PATH = 'path'
_DKEY_METADATA = 'metadata'
_DKEY_WIDTH = 'width'
_DKEY_HEIGHT = 'height'


def createCubePath(satStamp, bandNum, bandName, timeIntervalList, bboxList, crs):
    timeRange = 'S' + str(timeIntervalList[0]).replace('-', '') + 'E' + str(timeIntervalList[1]).replace('-', '')
    lonRange = 'LONS' + str(bboxList[0]).replace('.', 'c') + 'E' + str(bboxList[2]).replace('.', 'c')
    latRange = 'LATS' + str(bboxList[1]).replace('.', 'c') + 'E' + str(bboxList[3]).replace('.', 'c')

    # <SatelliteStamp>_<BandsNum>_<Type, e.g. RAW, NDVI>_<Timestamp>_<CRS>_<Longitudes>_<Latitudes>
    imgName = satStamp + '_B' + str(bandNum) + '_' + str(
        bandName) + '_' + timeRange + '_' + crs + '_' + lonRange + '_' + latRange
    return imgName


def readCubePathMetadata(path):
    metadataList = file_manip.pathFileName(path).split('.')[0].split('_')
    tmpIMG = rasterio.open(path)
    return {
        _DKEY_SATELLITE: metadataList[0],
        _DKEY_WIDTH: str(tmpIMG.width),
        _DKEY_HEIGHT: str(tmpIMG.height),
        _DKEY_BANDS: metadataList[1].split('B')[1],
        _DKEY_DATA_TYPE: metadataList[2],
        _DKEY_DATE_START: metadataList[3].split('S')[1].split('E')[0],
        _DKEY_DATE_END: metadataList[3].split('S')[1].split('E')[1],
        _DKEY_CRS: str(tmpIMG.crs),
        _DKEY_LONGITUDE_MIN: metadataList[5].split('LONS')[1].split('E')[0].replace('c', '.'),
        _DKEY_LONGITUDE_MAX: metadataList[5].split('LONS')[1].split('E')[1].replace('c', '.'),
        _DKEY_LATITUDE_MIN: metadataList[6].split('LATS')[1].split('E')[0].replace('c', '.'),
        _DKEY_LATITUDE_MAX: metadataList[6].split('LATS')[1].split('E')[1].replace('c', '.'),
    }


class MyDatacube:
    def __init__(self):
        self.cubeJSON = {}

    @staticmethod
    def exportIMG(imgPath, img, profile):
        with rasterio.open(imgPath, 'w', **profile) as dst:
            dst.write_band(1, img.astype(rasterio.float32))

    @staticmethod
    def viewIMG(imgPath):
        img = rasterio.open(imgPath).read(1)
        ep.plot_bands(img, cmap="RdYlGn", cols=1, vmin=-1, vmax=1)

    def createCube(self, baseFolder):
        list_of_dirs = file_manip.getListOfDirs(baseFolder)
        for _directory_ in list_of_dirs:
            self.cubeJSON[_directory_] = {}
            list_of_paths = file_manip.getListOfFiles(baseFolder + '/' + _directory_)
            _index_ = 0
            for _path_ in list_of_paths:
                metadata = readCubePathMetadata(_path_)
                self.cubeJSON[_directory_]['id_' + str(_index_).zfill(3)] = {
                    _DKEY_PATH: file_manip.normPath(_path_),
                    _DKEY_METADATA: metadata,
                }
                _index_ += 1

    def calculateNDVI_fromRAW(self):
        for _folderKey_ in self.cubeJSON.keys():
            _index_ = self.cubeJSON[_folderKey_].__len__()
            for _idKey_ in self.cubeJSON[_folderKey_].keys():
                filePath = self.cubeJSON[_folderKey_][_idKey_][_DKEY_PATH]
                metadata = self.cubeJSON[_folderKey_][_idKey_][_DKEY_METADATA]
                startDate = metadata[_DKEY_DATE_START]
                endDate = metadata[_DKEY_DATE_END]
                minLon = metadata[_DKEY_LONGITUDE_MIN]
                maxLon = metadata[_DKEY_LONGITUDE_MAX]
                minLat = metadata[_DKEY_LATITUDE_MIN]
                maxLat = metadata[_DKEY_LATITUDE_MAX]
                imgOpen = rasterio.open(filePath)
                profile = imgOpen.profile
                if evalScript.S02_L1C_STAMP in filePath and 'RAW' in filePath:
                    print(filePath)
                    bandRed = imgOpen.read(4)
                    bandNIR = imgOpen.read(8)
                    ndvi = (bandNIR - bandRed) / (bandNIR + bandRed)

                    fileName = createCubePath(
                        satStamp=evalScript.S02_L1C_STAMP,
                        bandNum=1,
                        bandName='NDVI',
                        timeIntervalList=[startDate, endDate],
                        bboxList=[minLon, minLat, maxLon, maxLat],
                        crs='WGS84')
                    exportPath = file_manip.normPath(filePath + '/../') + fileName + '.tif'
                    profile['dtype'] = 'float32'
                    profile['count'] = 1
                    self.exportIMG(exportPath, ndvi, profile)


if __name__ == "__main__":
    dc = MyDatacube()
    dc.createCube(MAIN_PATH)
    # dc.calculateNDVI_fromRAW()
    dc.viewIMG(TEST_IMG_NDVI_SHOW)