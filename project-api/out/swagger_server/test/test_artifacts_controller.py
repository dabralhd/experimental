# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.job_artifact import JobArtifact  # noqa: E501
from swagger_server.test import BaseTestCase


class TestArtifactsController(BaseTestCase):
    """ArtifactsController integration test stubs"""

    def test_app_download_activity_artifacts(self):
        """Test case for app_download_activity_artifacts

        Download Activity Job Artifacts
        """
        body = JobArtifact()
        response = self.client.open(
            '/projects/{project_name}/models/{model_name}/{activity_type}/artifacts'.format(project_name='project_name_example', model_name='model_name_example', activity_type='activity_type_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
