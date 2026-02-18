# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.project import Project  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProjectTemplatesController(BaseTestCase):
    """ProjectTemplatesController integration test stubs"""

    def test_app_get_templates_projects(self):
        """Test case for app_get_templates_projects

        Project templates list
        """
        response = self.client.open(
            '/templates/projects',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
