import lib.core.file_manipulation as file_manip

_PROJECT_FOLDER = file_manip.normPath(file_manip.realPath(__file__) + '/../../../')

ICON_CLOSE_PATH = _PROJECT_FOLDER + '/icon/exit_app_48x48.png'
ICON_NAVIGATE_PATH = _PROJECT_FOLDER + '/icon/optionNavigate_128x128.png'

STR_STORAGE_DEFAULT_PATH = file_manip.normPath(file_manip.PATH_DOCUMENTS + '/PocketGIS')

INT_MAX_STRETCH = 100000  # Spacer Max Stretch
