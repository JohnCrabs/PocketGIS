import rasterio
import lib.core.common.file_manipulation as file_manip
import lib.core.common.projectFuctions as projFunc

class GeotiffProcessing:
    def __init__(self):
        self._storagePath = ''
        self._imageCollectionJSON = {}

    def setStoragePath(self, path: str):
        self._storagePath = path

    def createImageCollectionJSON(self):
        listDir = file_manip.getListOfDirs(self._storagePath)
        for _dir_ in listDir:
            self._imageCollectionJSON[_dir_] = {}
            listFiles = file_manip.getListOfFiles(file_manip.normPath(self._storagePath + '/' + _dir_))
            for _file_ in listFiles:
                fileName = file_manip.pathFileName(_file_)
                metadata = projFunc.readCubePathMetadata(fileName)
                self._imageCollectionJSON[_dir_][fileName] = {
                    'full-path': file_manip.normPath(self._storagePath + '/' + _dir_ + '/' + fileName),
                    'metadata': metadata,
                }

