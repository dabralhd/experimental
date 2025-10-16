# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.applications_application_id_body import ApplicationsApplicationIdBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestApplicationsController(BaseTestCase):
    """ApplicationsController integration test stubs"""

    def test_app_delete_application_id(self):
        """Test case for app_delete_application_id

        Delete the application ID of a project
        """
        query_string = [('as_org', 'as_org_example')]
        response = self.client.open(
            '/projects/{project_name}/applications/{application_id}'.format(project_name='project_name_example', application_id='application_id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_update_application_id(self):
        """Test case for app_update_application_id

        Patch the application ID of a project
        """
        body = ApplicationsApplicationIdBody()
        query_string = [('as_org', 'as_org_example')]
        response = self.client.open(
            '/projects/{project_name}/applications/{application_id}'.format(project_name='project_name_example', application_id='application_id_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
