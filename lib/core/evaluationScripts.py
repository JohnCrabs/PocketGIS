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
