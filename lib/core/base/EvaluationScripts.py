import sentinelhub

import lib.core.common.file_manipulation as file_manip
import lib.core.common.projectFuctions as projFunc

# =========================== #
# ===== Dictionary Keys ===== #
# =========================== #

PKEY_SENTINEL_1_GRC = 'Sentinel-1-GRC'
PKEY_SENTINEL_2_L1C = 'Sentinel-2-L1C'
PKEY_SENTINEL_2_L2A = 'Sentinel-2-L2A'
PKEY_SENTINEL_3_OLCI = 'Sentinel-3-OLCI'
PKEY_SENTINEL_3_SLSTR = 'Sentinel-2-SLSTR'
PKEY_SENTINEL_5P = 'Sentinel-5P'

PKEY_LANDSAT_5 = 'Landsat-5'
PKEY_LANDSAT_7 = 'Landsat-7'
PKEY_LANDSAT_8 = 'Landsat-8'

SKEY_PATH_NAME = 'path-name'
SKEY_BANDS = 'bands'
SKEY_REQUEST_SCRIPT = 'request-script'
SKEY_REQUEST_VARIABLES = 'request-variables'
SKEY_AVAILABLE_PROCESSES = 'available-processes'

TKEY_S02_L1C_BAND_B01_COASTAL_AEROSOL = 'B01'
TKEY_S02_L1C_BAND_B02_BLUE = 'B02'
TKEY_S02_L1C_BAND_B03_GREEN = 'B03'
TKEY_S02_L1C_BAND_B04_RED = 'B04'
TKEY_S02_L1C_BAND_B05_VEGETATION_RED_EDGE_704 = 'B05'
TKEY_S02_L1C_BAND_B06_VEGETATION_RED_EDGE_740 = 'B06'
TKEY_S02_L1C_BAND_B07_VEGETATION_RED_EDGE_782 = 'B07'
TKEY_S02_L1C_BAND_B08_NIR = 'B08'
TKEY_S02_L1C_BAND_B08A_NARROW_NIR = 'B8A'
TKEY_S02_L1C_BAND_B09_WATER_VAPOUR = 'B09'
TKEY_S02_L1C_BAND_B10_SWIR_CIRRUS = 'B10'
TKEY_S02_L1C_BAND_B11_SWIR_1613 = 'B11'
TKEY_S02_L1C_BAND_B12_SWIR_2202 = 'B12'

TKEY_S05_BAND_CO = 'CO'
TKEY_S05_BAND_HCHO = 'HCHO'
TKEY_S05_BAND_NO2 = 'NO2'
TKEY_S05_BAND_O3 = 'O3'
TKEY_S05_BAND_SO2 = 'SO2'
TKEY_S05_BAND_CH4 = 'CH4'
TKEY_S05_BAND_AER_AI_340_380 = 'AER_AI_340_380'
TKEY_S05_BAND_AER_AI_354_388 = 'AER_AI_354_388'
TKEY_S05_BAND_CLOUD_BASE_PRESSURE = 'CLOUD_BASE_PRESSURE'
TKEY_S05_BAND_CLOUD_TOP_PRESSURE = 'CLOUD_TOP_PRESSURE'
TKEY_S05_BAND_CLOUD_BASE_HEIGHT = 'CLOUD_BASE_HEIGHT'
TKEY_S05_BAND_CLOUD_TOP_HEIGHT = 'CLOUD_TOP_HEIGHT'
TKEY_S05_BAND_CLOUD_OPTICAL_THICKNESS = 'CLOUD_OPTICAL_THICKNESS'
TKEY_S05_BAND_CLOUD_FRACTION = 'CLOUD_FRACTION'

TKEY_PROCESS_NDVI = 'NDVI'


# =================================== #
# ===== Dict Callable Functions ===== #
# =================================== #

# ----- Evaluation Script ----- #

def _func_S01_GRC_EvaluationScript():
    pass


def _func_S02_L1C_EvaluationScript(bandList):
    bands_str = ''
    bands_sample_str = ''
    for index in range(bandList.__len__()):
        tmp_band_str = '"' + bandList[index] + '"'
        tmp_sample_str = 'sample.' + bandList[index]

        if index == 0:
            bands_str += tmp_band_str
            bands_sample_str += tmp_sample_str
        else:
            bands_str += ',' + tmp_band_str
            bands_sample_str += ',' + tmp_sample_str

    return \
        f""" //VERSION=3
        function setup() {{
            return {{
                input: [{{
                    bands: [{bands_str}],
                    units: "DN"
                }}],
                output: {{
                    bands: {bandList.__len__()},
                    sampleType: "INT16"
                }}
            }};
        }}

        function evaluatePixel(sample) {{
            return [{bands_sample_str}];
        }}
        """


def _func_S02_L2A_EvaluationScript():
    pass


def _func_S03_OLCI_EvaluationScript():
    pass


def _func_S03_SLSTR_EvaluationScript():
    pass


def _func_S05_P_EvaluationScript():
    pass


def _func_LAN05_EvaluationScript():
    pass


def _func_LAN07_EvaluationScript():
    pass


def _func_LAN08_EvaluationScript():
    pass


# ----- Request Script ----- #
def _func_S01_GRC_RequestScript(storage_folder, bbox, size, config, bandList):
    pass


def _func_S02_L1C_RequestScript(storage_folder, bandList, timeIntervalList, sh_bbox, bbox_list, size, config, ):
    satelliteStampName = CONST_EVALUATION_DICTIONARY[PKEY_SENTINEL_2_L1C][SKEY_PATH_NAME]
    bandSize = bandList.__len__()
    data_folder = file_manip.normPath(storage_folder + '/' + satelliteStampName)
    file_manip.checkAndCreateFolders(data_folder)
    evalscript = _func_S02_L1C_EvaluationScript(bandList)

    for _timeSlot_ in timeIntervalList:
        newImageName = projFunc.createImagePathName(
            satStamp=satelliteStampName,
            bandNum=bandSize,
            dataType='RAW',
            timeIntervalList=_timeSlot_,
            bboxList=bbox_list,
            crs='WGS84',
            size=size)
        print("Image: " + newImageName + " is downloading!")
        request = sentinelhub.SentinelHubRequest(
            data_folder=data_folder,
            evalscript=evalscript,
            input_data=[
                sentinelhub.SentinelHubRequest.input_data(
                    data_collection=sentinelhub.DataCollection.SENTINEL2_L1C,
                    time_interval=_timeSlot_,
                    mosaicking_order='leastCC'
                )
            ],
            responses=[
                sentinelhub.SentinelHubRequest.output_response('default', sentinelhub.MimeType.TIFF)
            ],

            bbox=sh_bbox,
            size=size,
            config=config
        )
        request.save_data()
        projFunc.correctSentinelHubResponce(
            requestBaseDir=data_folder,
            newImageName=newImageName)


def _func_S02_L2A_RequestScript(storage_folder, bbox, size, config, bandList):
    pass


def _func_S03_OLCI_RequestScript(storage_folder, bbox, size, config, bandList):
    pass


def _func_S03_SLSTR_RequestScript(storage_folder, bbox, size, config, bandList):
    pass


def _func_S05_P_RequestScript(storage_folder, bbox, size, config, bandList):
    pass


def _func_LAN05_RequestScript(storage_folder, bbox, size, config, bandList):
    pass


def _func_LAN07_RequestScript(storage_folder, bbox, size, config, bandList):
    pass


def _func_LAN08_RequestScript(storage_folder, bbox, size, config, bandList):
    pass

# ----- Available Processes ----- #
def _process_calculate_NDVI(nir_band, red_band):
    return (nir_band - red_band) / (nir_band + red_band)

# =========================== #
# ===== Main Dictionary ===== #
# =========================== #

CONST_EVALUATION_DICTIONARY = {
    PKEY_SENTINEL_1_GRC: {
        SKEY_PATH_NAME: 'S01GRC',
        SKEY_BANDS: {

        },
        SKEY_REQUEST_SCRIPT: _func_S01_GRC_RequestScript,
        SKEY_AVAILABLE_PROCESSES: {

        }
    },
    PKEY_SENTINEL_2_L1C: {
        SKEY_PATH_NAME: 'S02L1C',
        SKEY_BANDS: {
            TKEY_S02_L1C_BAND_B01_COASTAL_AEROSOL: 'Coastal Aerosol',
            TKEY_S02_L1C_BAND_B02_BLUE: 'Blue',
            TKEY_S02_L1C_BAND_B03_GREEN: 'Green',
            TKEY_S02_L1C_BAND_B04_RED: 'Red',
            TKEY_S02_L1C_BAND_B05_VEGETATION_RED_EDGE_704: 'Vegetation Red Edge (~704nm)',
            TKEY_S02_L1C_BAND_B06_VEGETATION_RED_EDGE_740: 'Vegetation Red Edge (~740nm)',
            TKEY_S02_L1C_BAND_B07_VEGETATION_RED_EDGE_782: 'Vegetation Red Edge (~780nm)',
            TKEY_S02_L1C_BAND_B08_NIR: 'NIR',
            TKEY_S02_L1C_BAND_B08A_NARROW_NIR: 'Narrow NIR',
            TKEY_S02_L1C_BAND_B09_WATER_VAPOUR: 'Water Vapour',
            TKEY_S02_L1C_BAND_B10_SWIR_CIRRUS: 'SWIR-Cirrus',
            TKEY_S02_L1C_BAND_B11_SWIR_1613: 'SWIR (~1610nm)',
            TKEY_S02_L1C_BAND_B12_SWIR_2202: 'SWIR (~2200nm)',
        },
        SKEY_REQUEST_SCRIPT: _func_S02_L1C_RequestScript,
        SKEY_AVAILABLE_PROCESSES: {
            TKEY_PROCESS_NDVI: _process_calculate_NDVI
        }
    },
    PKEY_SENTINEL_2_L2A: {
        SKEY_PATH_NAME: 'S02L2A',
        SKEY_BANDS: {

        },
        SKEY_REQUEST_SCRIPT: _func_S02_L2A_RequestScript,
        SKEY_AVAILABLE_PROCESSES: {

        }
    },
    PKEY_SENTINEL_3_OLCI: {
        SKEY_PATH_NAME: 'S03OLCI',
        SKEY_BANDS: {

        },
        SKEY_REQUEST_SCRIPT: _func_S03_OLCI_RequestScript,
        SKEY_AVAILABLE_PROCESSES: {

        }
    },
    PKEY_SENTINEL_3_SLSTR: {
        SKEY_PATH_NAME: 'S03SLSTR',
        SKEY_BANDS: {

        },
        SKEY_REQUEST_SCRIPT: _func_S03_SLSTR_RequestScript,
        SKEY_AVAILABLE_PROCESSES: {

        }
    },
    PKEY_SENTINEL_5P: {
        SKEY_PATH_NAME: 'S05P',
        SKEY_BANDS: {
            TKEY_S05_BAND_CO: None,
            TKEY_S05_BAND_HCHO: None,
            TKEY_S05_BAND_NO2: None,
            TKEY_S05_BAND_O3: None,
            TKEY_S05_BAND_SO2: None,
            TKEY_S05_BAND_CH4: None,
            TKEY_S05_BAND_AER_AI_340_380: None,
            TKEY_S05_BAND_AER_AI_354_388: None,
            TKEY_S05_BAND_CLOUD_BASE_PRESSURE: None,
            TKEY_S05_BAND_CLOUD_TOP_PRESSURE: None,
            TKEY_S05_BAND_CLOUD_BASE_HEIGHT: None,
            TKEY_S05_BAND_CLOUD_TOP_HEIGHT: None,
            TKEY_S05_BAND_CLOUD_OPTICAL_THICKNESS: None,
            TKEY_S05_BAND_CLOUD_FRACTION: None
        },
        SKEY_REQUEST_SCRIPT: _func_S05_P_RequestScript,
        SKEY_AVAILABLE_PROCESSES: {

        }
    },
    PKEY_LANDSAT_5: {
        SKEY_PATH_NAME: 'LAN05',
        SKEY_BANDS: {

        },
        SKEY_REQUEST_SCRIPT: _func_LAN05_RequestScript,
        SKEY_AVAILABLE_PROCESSES: {

        }
    },
    PKEY_LANDSAT_7: {
        SKEY_PATH_NAME: 'LAN07',
        SKEY_BANDS: {

        },
        SKEY_REQUEST_SCRIPT: _func_LAN07_RequestScript,
        SKEY_AVAILABLE_PROCESSES: {

        }
    },
    PKEY_LANDSAT_8: {
        SKEY_PATH_NAME: 'LAN08',
        SKEY_BANDS: {

        },
        SKEY_REQUEST_SCRIPT: _func_LAN08_RequestScript,
        SKEY_AVAILABLE_PROCESSES: {

        }
    }
}

# -------------------------------------------------------------------------------------------------------------------------------- #

# Sentinel_2_L1C
S02_L1C_STAMP = 'S02L1C'

S02_L1C_BAND_B01_COASTAL_AEROSOL = 'B01'
S02_L1C_BAND_B02_BLUE = 'B02'
S02_L1C_BAND_B03_GREEN = 'B03'
S02_L1C_BAND_B04_RED = 'B04'
S02_L1C_BAND_B05_VEGETATION_RED_EDGE_704 = 'B05'
S02_L1C_BAND_B06_VEGETATION_RED_EDGE_740 = 'B06'
S02_L1C_BAND_B07_VEGETATION_RED_EDGE_782 = 'B07'
S02_L1C_BAND_B08_NIR = 'B08'
S02_L1C_BAND_B08A_NARROW_NIR = 'B8A'
S02_L1C_BAND_B09_WATER_VAPOUR = 'B09'
S02_L1C_BAND_B10_SWIR_CIRRUS = 'B10'
S02_L1C_BAND_B11_SWIR_1613 = 'B11'
S02_L1C_BAND_B12_SWIR_2202 = 'B12'

S02_L1C_BAND_LIST = [
    S02_L1C_BAND_B01_COASTAL_AEROSOL,
    S02_L1C_BAND_B02_BLUE,
    S02_L1C_BAND_B03_GREEN,
    S02_L1C_BAND_B04_RED,
    S02_L1C_BAND_B05_VEGETATION_RED_EDGE_704,
    S02_L1C_BAND_B06_VEGETATION_RED_EDGE_740,
    S02_L1C_BAND_B07_VEGETATION_RED_EDGE_782,
    S02_L1C_BAND_B08_NIR,
    S02_L1C_BAND_B08A_NARROW_NIR,
    S02_L1C_BAND_B09_WATER_VAPOUR,
    S02_L1C_BAND_B10_SWIR_CIRRUS,
    S02_L1C_BAND_B11_SWIR_1613,
    S02_L1C_BAND_B12_SWIR_2202
]


def ES_S02L1C(bandList: []):
    bands_str = ''
    bands_sample_str = ''
    for index in range(bandList.__len__()):
        tmp_band_str = '"' + bandList[index] + '"'
        tmp_sample_str = 'sample.' + bandList[index]

        if index == 0:
            bands_str += tmp_band_str
            bands_sample_str += tmp_sample_str
        else:
            bands_str += ',' + tmp_band_str
            bands_sample_str += ',' + tmp_sample_str

    return \
        f""" //VERSION=3
    function setup() {{
        return {{
            input: [{{
                bands: [{bands_str}],
                units: "DN"
            }}],
            output: {{
                bands: {bandList.__len__()},
                sampleType: "INT16"
            }}
        }};
    }}

    function evaluatePixel(sample) {{
        return [{bands_sample_str}];
    }}
    """


# Sentinel_5P
S05P_STAMP = 'S05P'

S05_BAND_CO = 'CO'
S05_BAND_HCHO = 'HCHO'
S05_BAND_NO2 = 'NO2'
S05_BAND_O3 = 'O3'
S05_BAND_SO2 = 'SO2'
S05_BAND_CH4 = 'CH4'
S05_BAND_AER_AI_340_380 = 'AER_AI_340_380'
S05_BAND_AER_AI_354_388 = 'AER_AI_354_388'
S05_BAND_CLOUD_BASE_PRESSURE = 'CLOUD_BASE_PRESSURE'
S05_BAND_CLOUD_TOP_PRESSURE = 'CLOUD_TOP_PRESSURE'
S05_BAND_CLOUD_BASE_HEIGHT = 'CLOUD_BASE_HEIGHT'
S05_BAND_CLOUD_TOP_HEIGHT = 'CLOUD_TOP_HEIGHT'
S05_BAND_CLOUD_OPTICAL_THICKNESS = 'CLOUD_OPTICAL_THICKNESS'
S05_BAND_CLOUD_FRACTION = 'CLOUD_FRACTION'

S05_BAND_LIST = [S05_BAND_CO,
                 S05_BAND_HCHO,
                 S05_BAND_NO2,
                 S05_BAND_O3,
                 S05_BAND_SO2,
                 S05_BAND_CH4,
                 S05_BAND_AER_AI_340_380,
                 S05_BAND_AER_AI_354_388,
                 S05_BAND_CLOUD_BASE_PRESSURE,
                 S05_BAND_CLOUD_TOP_PRESSURE,
                 S05_BAND_CLOUD_BASE_HEIGHT,
                 S05_BAND_CLOUD_TOP_HEIGHT,
                 S05_BAND_CLOUD_OPTICAL_THICKNESS,
                 S05_BAND_CLOUD_FRACTION
                 ]


def ES_S05P(band: str = 'CO'):
    return \
        f""" //VERSION=3
function setup() {{
    return {{
        input: [{{
            bands: ["{band}"],
            units: "DN"
        }}],
        output: {{
            bands: 1,
            sampleType: "FLOAT32"
        }}
    }};
}}

function evaluatePixel(sample) {{
    return [sample.{band}];
}}
"""


# Landsat_8_OLI_Level-1
LAN08OLIL1_STAMP = 'LAN08OLIL1'

LAN08_OLI_L1_BAND_B01_ULTRA_BLUE = 'B01'
LAN08_OLI_L1_BAND_B02_BLUE = 'B02'
LAN08_OLI_L1_BAND_B03_GREEN = 'B03'
LAN08_OLI_L1_BAND_B04_RED = 'B04'
LAN08_OLI_L1_BAND_B05_NIR = 'B05'
LAN08_OLI_L1_BAND_B06_SWIR_1 = 'B06'
LAN08_OLI_L1_BAND_B07_SWIR_2 = 'B07'
LAN08_OLI_L1_BAND_B08_PANCHROMATIC = 'B08'
LAN08_OLI_L1_BAND_B09_CIRRUS = 'B09'
LAN08_OLI_L1_BAND_B10_TIRS_1 = 'B10'
LAN08_OLI_L1_BAND_B11_TIRS_2 = 'B11'

LAN08_OLI_L1_BAND_LIST = [
    LAN08_OLI_L1_BAND_B01_ULTRA_BLUE,
    LAN08_OLI_L1_BAND_B02_BLUE,
    LAN08_OLI_L1_BAND_B03_GREEN,
    LAN08_OLI_L1_BAND_B04_RED,
    LAN08_OLI_L1_BAND_B05_NIR,
    LAN08_OLI_L1_BAND_B06_SWIR_1,
    LAN08_OLI_L1_BAND_B07_SWIR_2,
    LAN08_OLI_L1_BAND_B08_PANCHROMATIC,
    LAN08_OLI_L1_BAND_B09_CIRRUS,
    LAN08_OLI_L1_BAND_B10_TIRS_1,
    LAN08_OLI_L1_BAND_B11_TIRS_2
]

LAN08_OLI_L1_DICT_UNITS = {
    LAN08_OLI_L1_BAND_B01_ULTRA_BLUE: "REFLECTANCE",
    LAN08_OLI_L1_BAND_B02_BLUE: "REFLECTANCE",
    LAN08_OLI_L1_BAND_B03_GREEN: "REFLECTANCE",
    LAN08_OLI_L1_BAND_B04_RED: "REFLECTANCE",
    LAN08_OLI_L1_BAND_B05_NIR: "REFLECTANCE",
    LAN08_OLI_L1_BAND_B06_SWIR_1: "REFLECTANCE",
    LAN08_OLI_L1_BAND_B07_SWIR_2: "REFLECTANCE",
    LAN08_OLI_L1_BAND_B08_PANCHROMATIC: "REFLECTANCE",
    LAN08_OLI_L1_BAND_B09_CIRRUS: "REFLECTANCE",
    LAN08_OLI_L1_BAND_B10_TIRS_1: "BRIGHTNESS_TEMPERATURE",
    LAN08_OLI_L1_BAND_B11_TIRS_2: "BRIGHTNESS_TEMPERATURE"
}


def ES_LAN08_OLI_L1(bandList: []):
    bands_str = ''
    bands_sample_str = ''
    bands_units = ''
    for index in range(bandList.__len__()):
        tmp_band_str = '"' + bandList[index] + '"'
        tmp_sample_str = 'sample.' + bandList[index]
        tmp_band_unit_str = '"' + LAN08_OLI_L1_DICT_UNITS[bandList[index]] + '"'

        if index == 0:
            bands_str += tmp_band_str
            bands_sample_str += tmp_sample_str
            bands_units += tmp_band_unit_str
        else:
            bands_str += ',' + tmp_band_str
            bands_sample_str += ',' + tmp_sample_str
            bands_units += ',' + tmp_band_unit_str

    return \
        f""" //VERSION=3
    function setup() {{
        return {{
            input: [{{
                bands: [{bands_str}],
                units: [{bands_units}]
            }}],
            output: {{
                bands: {bandList.__len__()},
                sampleType: "UINT16"
            }}
        }};
    }}

    function evaluatePixel(sample) {{
        return [{bands_sample_str}];
    }}
    """
