
from project_api.vespucciprjmng.domain.log import DeviceDescription, Log
from project_api.vespucciprjmng.helpers.acquisition_folder_parser import (
    AcquisitionDescriptor,
    AcquisitionFolderParser,
)


class BoardAcquisition():

    @staticmethod
    def parse(board_log_folder: str) -> Log:
        """Parse acquisition folder and extract related information"""

        converted = False
        acquisition_descriptor: AcquisitionDescriptor = None
        try:
            acquisition_descriptor = AcquisitionFolderParser.standardv1(board_log_folder)
            converted = True
        except:
            print('Acquisition reading: Tentative #1 - standardv1 - failed') 

        if not converted:
            try:
                acquisition_descriptor = AcquisitionFolderParser.standardv2(board_log_folder)
                converted = True
            except:
                print('Acquisition reading: Tentative #2 - standardv2 - failed')   

            if not converted:
                try:
                    acquisition_descriptor = AcquisitionFolderParser.hsdatalog1(board_log_folder)
                    converted = True
                except:
                    print('Acquisition reading: Tentative #3 - hsdatalog1 - failed')   
                    raise Exception("Acquisition folder malformed: file descriptors are not recognized")

        log_domain_obj = Log()
        log_domain_obj.uuid         = acquisition_descriptor.uuid
        log_domain_obj.name         = acquisition_descriptor.name
        log_domain_obj.annotated    = acquisition_descriptor.annotated
        log_domain_obj.description  = acquisition_descriptor.description
        log_domain_obj.start_time   = acquisition_descriptor.start_date
        log_domain_obj.end_time     = acquisition_descriptor.end_date
        log_domain_obj.device_description = DeviceDescription(
            part_number=acquisition_descriptor.part_number,
            serial_number=acquisition_descriptor.serial_number,
            alias=acquisition_descriptor.alias,
            fw_name=acquisition_descriptor.fw_name,
            fw_version=acquisition_descriptor.fw_version,
            firmware_id=acquisition_descriptor.firmware_id,
            board_id=acquisition_descriptor.board_id
        )

        return log_domain_obj