import json
import os


class AcquisitionDescriptor():
    def __init__(
        self,
        uuid,
        name,
        part_number=None,
        serial_number=None,
        alias=None,
        fw_name=None,
        fw_version=None,
        board_id=None,
        firmware_id=None,
        start_date=None,
        end_date=None,
        annotated=None,
        description=None
    ):
        self.uuid           = uuid
        self.name           = name
        self.part_number    = part_number
        self.serial_number  = serial_number
        self.alias          = alias
        self.fw_name        = fw_name
        self.fw_version     = fw_version
        self.board_id       = board_id
        self.firmware_id    = firmware_id
        self.start_date     = start_date
        self.end_date       = end_date
        self.annotated      = annotated
        self.description    = description


class AcquisitionFolderParser():

    @staticmethod
    def hsdatalog1(base_path):
        acquisition_info_config_path =  os.path.join(base_path, "AcquisitionInfo.json")
        device_config_path =  os.path.join(base_path, "DeviceConfig.json")

        uuid        = None
        name        = None
        start_date  = None
        end_date    = None
        annotated   = None
        description = None

        part_number     = None
        serial_number   = None
        alias           = None
        fw_name         = None
        fw_version      = None

        # 1. Parsing acquisition info json file
        with open(acquisition_info_config_path) as f:
            acquisition_info = json.load(f)
            uuid        = acquisition_info["UUIDAcquisition"]
            name = acquisition_info["Name"]
            start_date  = acquisition_info["start_time"]
            description = acquisition_info["Description"]
            if "annotated" in acquisition_info:
                annotated = acquisition_info["annotated"]
            elif "Tags" in acquisition_info:
                annotated   = len(acquisition_info["Tags"]) > 0
            else:
                annotated = False
            if "end_time" in acquisition_info:
                end_date = acquisition_info["end_time"]

        # 2. Parsing device config json file
        with open(device_config_path) as f:
            device_config = json.load(f)
            part_number     = device_config["device"]["deviceInfo"]["partNumber"]
            serial_number   = device_config["device"]["deviceInfo"]["serialNumber"]
            alias           = device_config["device"]["deviceInfo"]["alias"]
            fw_name         = device_config["device"]["deviceInfo"]["fwName"]
            fw_version      = device_config["device"]["deviceInfo"]["fwVersion"]
        
        return AcquisitionDescriptor(uuid=uuid, name=name, part_number=part_number, serial_number=serial_number, alias=alias, fw_name=fw_name, fw_version=fw_version, start_date=start_date, end_date=end_date, annotated=annotated, description=description)


    @staticmethod
    def standardv1(base_path):
        acquisition_info_config_path =  os.path.join(base_path, "acquisition_info.json")
        device_config_path =  os.path.join(base_path, "device_config.json")

        uuid        = None
        name        = None
        start_date  = None
        end_date    = None
        annotated   = None
        description = None

        part_number     = None
        serial_number   = None
        alias           = None
        fw_name         = None
        fw_version      = None

        # 1. Parsing acquisition info json file
        with open(acquisition_info_config_path) as f:
            acquisition_info = json.load(f)
            uuid        = acquisition_info["uuid"]
            name        = acquisition_info["name"]
            description = acquisition_info["description"]
            start_date  = acquisition_info["start_time"]
            if "annotated" in acquisition_info:
                annotated = acquisition_info["annotated"]
            elif "tags" in acquisition_info:
                annotated   = len(acquisition_info["tags"]) > 0
            else:
                annotated = False
            if "end_time" in acquisition_info:
                end_date = acquisition_info["end_time"]

        # 2. Parsing device config json file
        with open(device_config_path) as f:
            device_config = json.load(f)
            part_number     = device_config["device"]["device_info"]["part_number"]
            serial_number   = device_config["device"]["device_info"]["serial_number"]
            alias           = device_config["device"]["device_info"]["alias"]
            fw_name         = device_config["device"]["device_info"]["fw_name"]
            fw_version      = device_config["device"]["device_info"]["fw_version"]
        
        return AcquisitionDescriptor(uuid=uuid, name=name, part_number=part_number, serial_number=serial_number, alias=alias, fw_name=fw_name, fw_version=fw_version, start_date=start_date, end_date=end_date, annotated=annotated, description=description)

    @staticmethod
    def standardv2(base_path):
        acquisition_info_config_path =  os.path.join(base_path, "acquisition_info.json")
        device_config_path =  os.path.join(base_path, "device_config.json")

        uuid        = None
        name        = None
        start_date  = None
        end_date    = None
        annotated   = None
        description = None

        board_id        = None
        firmware_id     = None

        serial_number   = None
        alias           = None
        fw_name         = None
        fw_version      = None
        part_number     = None

        # 1. Parsing acquisition info json file
        with open(acquisition_info_config_path) as f:
            acquisition_info = json.load(f)
            uuid        = acquisition_info["uuid"]
            name        = acquisition_info["name"]
            description = acquisition_info["description"]
            start_date  = acquisition_info["start_time"]
            annotated   = len(acquisition_info["tags"]) > 0
            if "annotated" in acquisition_info:
                annotated = acquisition_info["annotated"]
            elif "tags" in acquisition_info:
                annotated   = len(acquisition_info["tags"]) > 0
            else:
                annotated = False

            if "end_time" in acquisition_info:
                end_date = acquisition_info["end_time"]

        # 2. Parsing device config json file
        with open(device_config_path) as f:
            device_config = json.load(f)

            serial_number   = device_config["devices"][0]["sn"]
            board_id        = device_config["devices"][0]["board_id"]
            firmware_id     = device_config["devices"][0]["fw_id"]

            for c in device_config["devices"][0]["components"]:
                if "firmware_info" in c:
                    alias           = c["firmware_info"]["alias"]
                    fw_name         = c["firmware_info"]["fw_name"]
                    fw_version      = c["firmware_info"]["fw_version"]
                    if "part_number" in c["firmware_info"]:
                        part_number = c["firmware_info"]["part_number"]
                        
                                
        return AcquisitionDescriptor(uuid=uuid, name=name, board_id=board_id, firmware_id=firmware_id, start_date=start_date, end_date=end_date, annotated=annotated, description=description, serial_number=serial_number, alias=alias, fw_name=fw_name, fw_version=fw_version, part_number=part_number)