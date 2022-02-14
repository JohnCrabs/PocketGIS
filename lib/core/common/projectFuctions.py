import lib.core.common.projectFlags as projFlags
import lib.core.common.file_manipulation as file_manip


def createImagePathName(satStamp, bandNum, dataType, timeIntervalList, bboxList, crs, size):
    timeRange = 'S' + str(timeIntervalList[0]).replace('-', '') + 'E' + str(timeIntervalList[1]).replace('-', '')
    latRange = 'LATS' + str(bboxList[0]).replace('.', 'c') + 'E' + str(bboxList[2]).replace('.', 'c')
    lonRange = 'LONS' + str(bboxList[1]).replace('.', 'c') + 'E' + str(bboxList[3]).replace('.', 'c')
    imageSize = 'W' + str(size[0]) + 'H' + str(size[1])

    # <SatelliteStamp>_<BandsNum>_<Type, e.g. RAW, NDVI>_<Timestamp>_<CRS>_<Latitudes>_<Longitudes>_<imageSize>
    imgName = satStamp + '_B' + str(bandNum) + '_' + \
              str(dataType) + '_' + timeRange + '_' + crs + '_' + \
              latRange + '_' + lonRange + '_' + imageSize
    return imgName


def readCubePathMetadata(path):
    metadataList = file_manip.pathFileName(path).split('.')[0].split('_')
    return {
        projFlags.DKEY_PATH_SATELLITE: metadataList[0],
        projFlags.DKEY_PATH_BANDS: metadataList[1].split('B')[1],
        projFlags.DKEY_PATH_DATA_TYPE: metadataList[2],
        projFlags.DKEY_PATH_DATE_START: metadataList[3].split('S')[1].split('E')[0],
        projFlags.DKEY_PATH_DATE_END: metadataList[3].split('S')[1].split('E')[1],
        projFlags.DKEY_PATH_CRS: metadataList[4],
        projFlags.DKEY_PATH_LATITUDE_MIN: metadataList[5].split('LATS')[1].split('E')[0].replace('c', '.'),
        projFlags.DKEY_PATH_LATITUDE_MAX: metadataList[5].split('LATS')[1].split('E')[1].replace('c', '.'),
        projFlags.DKEY_PATH_LONGITUDE_MIN: metadataList[6].split('LONS')[1].split('E')[0].replace('c', '.'),
        projFlags.DKEY_PATH_LONGITUDE_MAX: metadataList[6].split('LONS')[1].split('E')[1].replace('c', '.'),
        projFlags.DKEY_PATH_WIDTH: metadataList[6].split('W')[1].split('H')[0],
        projFlags.DKEY_PATH_HEIGHT: metadataList[6].split('W')[1].split('H')[1],
    }


def correctSentinelHubResponce(requestBaseDir, newImageName):
    list_of_path = file_manip.getListOfFiles(requestBaseDir)
    for filePath in list_of_path:
        # Get only Sentinel Hub response:
        if 'response' in filePath:
            suffix = file_manip.pathFileSuffix(filePath)
            file_manip.copyfile(filePath, filePath + '/../../' + newImageName + suffix)
            file_manip.removeDirectoryAndItsFiles(filePath + '/../')
