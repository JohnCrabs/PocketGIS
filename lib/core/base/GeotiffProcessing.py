import rasterio


class GeotiffProcessing:
    def __init__(self):
        self._storagePath = ''

    def setStoragePath(self, path: str):
        self._storagePath = path

