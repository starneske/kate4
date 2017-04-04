#!/usr/bin/python
"""
Add docstring here
"""
from flask_restful_swagger_2 import Resource, swagger

from qube.src.api.swagger_models.kate4 import VersionModel
from qube.src.api.swagger_models.response_messages import \
    ErrorModel, response_msgs
from qube.src.commons.log import Log as LOG
from qube.src.commons.qube_config import QubeConfig

EMPTY = ''


class kate4ItemVersionController(Resource):
    def __init__(self, *args, **kwargs):
        super(kate4ItemVersionController, self).__init__(*args, **kwargs)
        self.config = QubeConfig.get_config()

    @swagger.doc(
        {
            'tags': ['kate4'],
            'description': 'kate4 Version operation',
            'responses': response_msgs
        }
    )
    def get(self):
        """gets an kate4 item that omar has changed
        """
        try:
            LOG.debug("Get version ")
            return VersionModel(**{'version': self.config.get_version()}), 200
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'message': ex}), 500
