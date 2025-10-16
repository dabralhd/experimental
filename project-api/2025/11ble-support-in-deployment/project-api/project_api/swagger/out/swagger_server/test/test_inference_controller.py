# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.patch_inference_model_reference import PatchInferenceModelReference  # noqa: E501
from swagger_server.test import BaseTestCase


class TestInferenceController(BaseTestCase):
    """InferenceController integration test stubs"""

    def test_app_patch_leaf_inference_model(self):
        """Test case for app_patch_leaf_inference_model

        Patch inference model reference for a leaf device
        """
        body = PatchInferenceModelReference()
        response = self.client.open(
            '/projects/{project_name}/deployments/{deployment_id}/leaf/{device_id}/inference'.format(project_name='project_name_example', deployment_id='deployment_id_example', device_id='device_id_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
