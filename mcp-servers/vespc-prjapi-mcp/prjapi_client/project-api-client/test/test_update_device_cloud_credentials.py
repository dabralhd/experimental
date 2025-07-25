# coding: utf-8

"""
    STAIoTCraft - Project API

    REST API to access STAIoTCraft Back-End web-service User Projects

    The version of the OpenAPI document: 3.0.7
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from project_api_client.models.update_device_cloud_credentials import UpdateDeviceCloudCredentials

class TestUpdateDeviceCloudCredentials(unittest.TestCase):
    """UpdateDeviceCloudCredentials unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UpdateDeviceCloudCredentials:
        """Test UpdateDeviceCloudCredentials
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UpdateDeviceCloudCredentials`
        """
        model = UpdateDeviceCloudCredentials()
        if include_optional:
            return UpdateDeviceCloudCredentials(
                id = ''
            )
        else:
            return UpdateDeviceCloudCredentials(
        )
        """

    def testUpdateDeviceCloudCredentials(self):
        """Test UpdateDeviceCloudCredentials"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
