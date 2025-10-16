# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestDeploymentArtifactsController(BaseTestCase):
    """DeploymentArtifactsController integration test stubs"""

    def test_get_artifacts(self):
        """Test case for get_artifacts

        Get deployment artifacts of a project
        """
        query_string = [('log_uuid', 'log_uuid_example'),
                        ('as_org', 'as_org_example')]
        response = self.client.open(
            '/projects/{project_name}/deployments/{deployment_name}/devices/{device_id}/artifacts'.format(project_name='project_name_example', deployment_name='deployment_name_example', device_id='device_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
