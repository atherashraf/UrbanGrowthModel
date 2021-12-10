import json
from typing import OrderedDict

from sentinelsat import SentinelAPI
from app.config.utils import ConfigUtils
from app.local_settings import IMAGES_PATH
from app.models.main_dt import SentinelDataInfo


class SentinelUtils:
    api: SentinelAPI
    product_info: OrderedDict

    def __init__(self):
        config_utils = ConfigUtils()
        sentinel_user = config_utils.get_data('sentinel_user')
        sentinel_password = config_utils.get_data('sentinel_password')
        self.api = SentinelAPI(sentinel_user, sentinel_password, 'https://apihub.copernicus.eu/apihub')

    def download_by_aoi(self, info: SentinelDataInfo):
        aoi = info.aoi
        self.products_info = self.api.query(aoi,
                                            date=(info.start_date, info.end_date),
                                            platformname=info.platformname,
                                            cloudcoverpercentage=(0, 30))
        # product_ids = list(self.products_info.keys())
        # info = self.api.get_footprints()
        # print(info)
        for id in self.products_info.keys():
            try:
                # summary = json.loads(self.products_info[id]['summary'])
                print("id", id)
                self.api.download(id, directory_path=IMAGES_PATH)
                break
            except Exception as e:
                print("error", str(e))
