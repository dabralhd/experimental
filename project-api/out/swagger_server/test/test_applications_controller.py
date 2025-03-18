# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestApplicationsController(BaseTestCase):
    """ApplicationsController integration test stubs"""

    def test_app_delete_application_id(self):
        """Test case for app_delete_application_id

        Delete the application ID of a project
        """
        response = self.client.open(
            '/projects/{project_name}/applications/{application_id}'.format(project_name='project_name_example', application_id='application_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
