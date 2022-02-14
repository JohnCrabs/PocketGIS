import sentinelhub
import datetime as dt

import lib.core.base.EvaluationScripts as evalScript

_KEY_INSTANCE_ID = 'instance-id'
_KEY_CLIENT_ID = 'client-id'
_KEY_CLIENT_SECRET = 'client-secret'


class SentinelHubDownloader:
    def __init__(self):
        self._storagePath = ''
        self._sh_config_credentials_list = {
            _KEY_INSTANCE_ID: '',
            _KEY_CLIENT_ID: '',
            _KEY_CLIENT_SECRET: ''
        }
        self._sh_config = sentinelhub.SHConfig()
        self._timeSlots = []

        self._bbox_wgs84 = []
        self._bbox_sh = None
        self._spatial_resolution = None
        self._image_resolution = None

    def setStoragePath(self, path: str):
        self._storagePath = path

    def setSentinelHubConfiguration(self, instance_id, client_id, client_secret):
        """
        Set the configuration credentials, which needed for connection to Sentinel-Hub.
        :param instance_id: Parameter instance_id is used when using OGC endpoints of the Sentinel Hub services.
                            It is the identifier of a configuration users can set up in the Sentinel Hub Dashboard
                            under “Configuration Utility”.
        :param client_id: Can be created in the Sentinel Hub Dashboard under “User settings”. IS needed when accessing
                          protected endpoints of the service (Process, Catalog, Batch, BYOC, and other APIs). There is
                          “OAuth clients” frame where we can create a new OAuth client.
        :param client_secret: Can be created in the Sentinel Hub Dashboard under “User settings”. IS needed when accessing
                              protected endpoints of the service (Process, Catalog, Batch, BYOC, and other APIs). There is
                              “OAuth clients” frame where we can create a new OAuth client.
        :return: Nothing
        """
        self._sh_config_credentials_list[_KEY_INSTANCE_ID] = instance_id
        self._sh_config_credentials_list[_KEY_CLIENT_ID] = client_id
        self._sh_config_credentials_list[_KEY_CLIENT_SECRET] = client_secret

        self._sh_config.instance_id = self._sh_config_credentials_list[_KEY_INSTANCE_ID]
        self._sh_config.sh_client_id = self._sh_config_credentials_list[_KEY_CLIENT_ID]
        self._sh_config.sh_client_secret = self._sh_config_credentials_list[_KEY_CLIENT_SECRET]

    def _createSentinelHubConfig(self):
        pass

    def setTimeSlots(self,
                     startYear: int, startMonth: int, startDay: int,
                     endYear: int, endMonth: int, endDay: int,
                     n_chunks: int
                     ):
        startDate = dt.datetime(year=startYear, month=startMonth, day=startDay)
        endDate = dt.datetime(year=endYear, month=endMonth, day=endDay)
        deltaTime = (endDate - startDate) / n_chunks
        edges = [(startDate + i * deltaTime).date().isoformat() for i in range(n_chunks + 1)]
        self._timeSlots = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

    def setAreaOfInterest(self,
                          minLatitude: float, minLongitude: float,
                          maxLatitude: float, maxLongitude: float,
                          spatialResolution: float
                          ):
        self._bbox_wgs84 = [minLatitude, minLongitude, maxLatitude, maxLongitude]
        self._spatial_resolution = spatialResolution

        self._bbox_sh = sentinelhub.BBox(bbox=self._bbox_wgs84, crs=sentinelhub.CRS.WGS84)
        self._image_resolution = sentinelhub.bbox_to_dimensions(self._bbox_sh, resolution=self._spatial_resolution)

    def imgDownload(self, downloadJSON):
        for _key_ in downloadJSON.keys():
            evalScript.CONST_EVALUATION_DICTIONARY[_key_][evalScript.SKEY_REQUEST_SCRIPT](
                storage_folder=self._storagePath,
                bandList=downloadJSON[_key_],
                timeIntervalList=self._timeSlots,
                sh_bbox=self._bbox_sh,
                bbox_list=self._bbox_wgs84,
                size=self._image_resolution,
                config=self._sh_config
            )
