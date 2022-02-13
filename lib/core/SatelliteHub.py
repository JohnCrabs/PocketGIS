import sentinelhub
import logging
import lib.core.SentinelHubAuth as sha

import lib.core.file_manipulation as file_manip
import lib.core.EvaluationScripts as evalScr

import datetime as dt

from lib.core.myDatacube import createCubePath

# from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
#     DataCollection, bbox_to_dimensions, DownloadRequest

from lib.core.plotImage import plot_image


# Create a class named SatelliteHub which uses the SentinelHub framework for downloading new image files
class SatelliteHub:
    def __init__(self):
        self._sh_wgs84 = []
        self._resolution_in_meters = 60
        self._image_bbox = None
        self._image_size = None
        self._image_request = None
        self._image = None
        self._timeSlots = []

    @staticmethod
    def config():
        config = sentinelhub.SHConfig()
        config.instance_id = sha.INSTANCE_ID
        config.sh_client_id = sha.CLIENT_ID
        config.sh_client_secret = sha.CLIENT_SECRET
        if not config.sh_client_id or not config.sh_client_secret:
            print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")
        else:
            print("Successful Configuration!")

        return config

    @staticmethod
    def logging():
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(levelname)s:%(name)s:%(threadName)s:%(message)s',
        )

    @staticmethod
    def _correctResponce(requestPath, imgName):
        list_of_path = file_manip.getListOfFiles(requestPath)
        for filePath in list_of_path:
            suffix = file_manip.pathFileSuffix(filePath)
            # if suffix != '.json':
            if 'response' in filePath:
                file_manip.copyfile(filePath, filePath + '/../../' + imgName + suffix)
        file_manip.removeDirectoryAndItsFiles(list_of_path[0] + '/../')

    def set_TimeSlots(self, startYear: int, startMonth: int, startDay: int,
                      endYear: int, endMonth: int, endDay: int,
                      n_chunks: int, prt_Slots=True):
        start = dt.datetime(startYear, startMonth, startDay)
        end = dt.datetime(endYear, endMonth, endDay)
        tDelta = (end - start) / n_chunks
        edges = [(start + i * tDelta).date().isoformat() for i in range(n_chunks + 1)]
        self._timeSlots = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
        if prt_Slots:
            print("Slot Ranges:")
            for timeSlot in self._timeSlots:
                print(timeSlot[0] + ' - ' + timeSlot[1])

    # longitude and latitude coordinates of lower left and upper right corners
    def set_WGS84(self, min_llc_lon, min_llc_lat, max_urc_lon, max_urc_lat):
        self._sh_wgs84 = [min_llc_lon, min_llc_lat, max_urc_lon, max_urc_lat]

    def set_ResolutionInMeters(self, res_in_meters):
        self._resolution_in_meters = res_in_meters

    def calc_ImageSize(self):
        self._image_bbox = sentinelhub.BBox(bbox=self._sh_wgs84, crs=sentinelhub.CRS.WGS84)
        self._image_size = sentinelhub.bbox_to_dimensions(self._image_bbox, resolution=self._resolution_in_meters)

        print(f'Image shape at {self._resolution_in_meters} m resolution: {self._image_size} pixels')

    def getDem(self):
        evalscript_dem = '''
        //VERSION=3
        function setup() {
          return {
            input: ["DEM"],
            output:{
              id: "default",
              bands: 1,
              sampleType: SampleType.FLOAT32
            }
          }
        }

        function evaluatePixel(sample) {
          return [sample.DEM]
        }
        '''
        self._image_request = sentinelhub.SentinelHubRequest(
            data_folder='../../',
            evalscript=evalscript_dem,
            input_data=[
                sentinelhub.SentinelHubRequest.input_data(
                    data_collection=sentinelhub.DataCollection.DEM,
                    time_interval=('2020-07-01', '2020-07-15'),
                )
            ],
            responses=[
                sentinelhub.SentinelHubRequest.output_response('default', sentinelhub.MimeType.TIFF)
            ],
            bbox=self._image_bbox,
            size=self._image_size,
            config=self.config()
        )
        self._image = self._image_request.get_data()
        self._image_request.save_data()

    def getMultipleImages(self):
        start = dt.datetime(2020, 6, 1)
        end = dt.datetime(2020, 8, 31)
        n_chunks = 13
        tdelta = (end - start) / n_chunks
        edges = [(start + i * tdelta).date().isoformat() for i in range(n_chunks)]
        slots = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

        print('Monthly time windows:\n')
        for slot in slots:
            print(slot)

        evalscript_all_bands = """
                    //VERSION=3
                    function setup() {
                        return {
                            input: [{
                                bands: ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B10","B11","B12"],
                                units: "DN"
                            }],
                            output: {
                                bands: 13,
                                sampleType: "INT16"
                            }
                        };
                    }

                    function evaluatePixel(sample) {
                        return [sample.B01,
                                sample.B02,
                                sample.B03,
                                sample.B04,
                                sample.B05,
                                sample.B06,
                                sample.B07,
                                sample.B08,
                                sample.B8A,
                                sample.B09,
                                sample.B10,
                                sample.B11,
                                sample.B12];
                    }
                """

        # create a list of requests
        list_of_requests = []

        baseFolder = '../../Download/'

        for time_interval in slots:
            data_folder = baseFolder + '/' + time_interval[0] + '_' + time_interval[1] + '/'
            file_manip.checkAndCreateFolder(data_folder)
            request = sentinelhub.SentinelHubRequest(
                data_folder=data_folder,
                evalscript=evalscript_all_bands,
                input_data=[
                    sentinelhub.SentinelHubRequest.input_data(
                        data_collection=sentinelhub.DataCollection.SENTINEL2_L1C,
                        time_interval=time_interval,
                        mosaicking_order='leastCC'
                    )
                ],
                responses=[
                    sentinelhub.SentinelHubRequest.output_response('default', sentinelhub.MimeType.TIFF)
                ],
                bbox=self._image_bbox,
                size=self._image_size,
                config=self.config()
            )

            list_of_requests.append(request)

        # list_of_requests = [request.save_data() for request in list_of_requests]

        # download data with multiple threads
        # data = sentinelhub.SentinelHubDownloadClient(config=self.config()).download(list_of_requests, max_threads=5)

    def getAllSentinel_5P_Data(self):
        # list_of_requests = []
        startDate = self._timeSlots[0][0]
        endDate = self._timeSlots[self._timeSlots.__len__() - 1][1]
        baseFolder = file_manip.PATH_DOCUMENTS + '/PocketGIS/' + startDate + '_' + endDate + '/Sentinel_5P/'
        for band in evalScr.S05_BAND_LIST:
            evaluation_script = evalScr.ES_S05P(band=band)
            print(evaluation_script)
            bandFolder = baseFolder + band + '/'
            for timeIntervalSlot in self._timeSlots:
                timeRange = str(timeIntervalSlot[0]).replace('-', '') + '_' + str(timeIntervalSlot[1]).replace('-', '')
                slotFolder = bandFolder + timeRange + '/'
                file_manip.checkAndCreateFolders(slotFolder)
                request = sentinelhub.SentinelHubRequest(
                    data_folder=slotFolder,
                    evalscript=evaluation_script,
                    input_data=[
                        sentinelhub.SentinelHubRequest.input_data(
                            data_collection=sentinelhub.DataCollection.SENTINEL5P,
                            time_interval=timeIntervalSlot,
                            mosaicking_order='mostRecent'
                        )
                    ],
                    responses=[
                        sentinelhub.SentinelHubRequest.output_response('default', sentinelhub.MimeType.TIFF)
                    ],
                    bbox=self._image_bbox,
                    size=self._image_size,
                    config=self.config()
                )
                print('Download images for band: {}, and time-range: {}'.format(band, timeRange))
                request.save_data()
                self._correctResponce(slotFolder, band)
        print('Process Finished Successfully!')

    def getAllSentinel_2L1C_Data(self):
        # list_of_requests = []
        startDate = self._timeSlots[0][0]
        endDate = self._timeSlots[self._timeSlots.__len__() - 1][1]
        baseFolder = file_manip.PATH_DOCUMENTS + '/PocketGIS/' + evalScr.S02_L1C_STAMP
        evaluation_script = evalScr.ES_S02L1C(bandList=evalScr.S02_L1C_BAND_LIST)
        file_manip.checkAndCreateFolders(baseFolder)
        print(evaluation_script)
        for timeIntervalSlot in self._timeSlots:
            timeRange = 'S' + str(timeIntervalSlot[0]).replace('-', '') + 'E' + str(timeIntervalSlot[1]).replace('-', '')
            slotFolder = baseFolder + '/'

            # <SatelliteStamp>_<BandsNum>_<Type, e.g. RAW, NDVI>_<Timestamp>_<CRS>_<Longitudes>_<Latitudes>
            imgName = createCubePath(satStamp=evalScr.S02_L1C_STAMP,
                                     bandNum=13,
                                     bandName='RAW',
                                     timeIntervalList=timeIntervalSlot,
                                     bboxList=self._sh_wgs84,
                                     crs='WGS84')

            file_manip.checkAndCreateFolders(slotFolder)
            request = sentinelhub.SentinelHubRequest(
                data_folder=slotFolder,
                evalscript=evaluation_script,
                input_data=[
                    sentinelhub.SentinelHubRequest.input_data(
                        data_collection=sentinelhub.DataCollection.SENTINEL2_L1C,
                        time_interval=timeIntervalSlot,
                        mosaicking_order='leastCC'
                    )
                ],
                responses=[
                    sentinelhub.SentinelHubRequest.output_response('default', sentinelhub.MimeType.TIFF)
                ],
                bbox=self._image_bbox,
                size=self._image_size,
                config=self.config()
            )
            print('Download image for time-range: {}'.format(timeRange))
            request.save_data()
            self._correctResponce(slotFolder, imgName)
        print('Process Finished Successfully!')

    def getAllLandsat_8_OLI_L1_Data(self):
        # list_of_requests = []
        startDate = self._timeSlots[0][0]
        endDate = self._timeSlots[self._timeSlots.__len__() - 1][1]
        baseFolder = file_manip.PATH_DOCUMENTS + '/PocketGIS/' + startDate + '_' + endDate + '/Landsat_8_OLI_L1/'
        evaluation_script = evalScr.ES_LAN08_OLI_L1(bandList=evalScr.LAN08_OLI_L1_BAND_LIST)
        print(evaluation_script)
        for timeIntervalSlot in self._timeSlots:
            timeRange = str(timeIntervalSlot[0]).replace('-', '') + '_' + str(timeIntervalSlot[1]).replace('-', '')
            slotFolder = baseFolder + timeRange + '/'
            file_manip.checkAndCreateFolders(slotFolder)
            request = sentinelhub.SentinelHubRequest(
                data_folder=slotFolder,
                evalscript=evaluation_script,
                input_data=[
                    sentinelhub.SentinelHubRequest.input_data(
                        data_collection=sentinelhub.DataCollection.LANDSAT_OT_L1,
                        time_interval=timeIntervalSlot,
                        mosaicking_order='leastCC'
                    )
                ],
                responses=[
                    sentinelhub.SentinelHubRequest.output_response('default', sentinelhub.MimeType.TIFF)
                ],
                bbox=self._image_bbox,
                size=self._image_size,
                config=self.config()
            )
            print('Download image for time-range: {}'.format(timeRange))
            request.save_data()
            self._correctResponce(slotFolder, 'LAN08_OLI_L1')
        print('Process Finished Successfully!')

    def showImage(self):
        image = self._image[0]
        print(f'Image type: {image.dtype}')

        # plot function
        # factor 1/255 to scale between 0-1
        # factor 3.5 to increase brightness
        plot_image(image, factor=3.5 / 255, clip_range=(0, 1))


if __name__ == "__main__":
    satHub = SatelliteHub()
    Athens = {'min_lon': 23.70,
              'min_lat': 37.95,
              'max_lon': 23.75,
              'max_lat': 38.00
              }

    Piraeus = {'min_lon': 23.61,
               'min_lat': 37.93,
               'max_lon': 23.66,
               'max_lat': 37.98,
               }

    satHub.set_WGS84(min_llc_lon=Piraeus['min_lon'],
                     min_llc_lat=Piraeus['min_lat'],
                     max_urc_lon=Piraeus['max_lon'],
                     max_urc_lat=Piraeus['max_lat'])

    satHub.set_ResolutionInMeters(res_in_meters=2.5)
    satHub.calc_ImageSize()
    satHub.set_TimeSlots(startYear=2021, startMonth=1, startDay=1,
                         endYear=2021, endMonth=12, endDay=31, n_chunks=52)
    # satHub.getTrueColor()
    # satHub.getAllSentinel_5P_Data()
    satHub.getAllSentinel_2L1C_Data()
    # satHub.getAllLandsat_8_OLI_L1_Data()
