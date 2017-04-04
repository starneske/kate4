#!/usr/bin/python
"""
Add docstring here
"""
from flask import request
from flask_restful_swagger_2 import Resource, swagger
from mongoalchemy.exceptions import ExtraValueException

from qube.src.api.decorators import login_required
from qube.src.api.swagger_models.kate4 import kate4Model # noqa: ignore=I100
from qube.src.api.swagger_models.kate4 import kate4ModelPost # noqa: ignore=I100
from qube.src.api.swagger_models.kate4 import kate4ModelPostResponse # noqa: ignore=I100
from qube.src.api.swagger_models.kate4 import kate4ModelPut # noqa: ignore=I100

from qube.src.api.swagger_models.parameters import (
    body_post_ex, body_put_ex, header_ex, path_ex, query_ex)
from qube.src.api.swagger_models.response_messages import (
    del_response_msgs, ErrorModel, get_response_msgs, post_response_msgs,
    put_response_msgs)
from qube.src.commons.error import kate4ServiceError
from qube.src.commons.log import Log as LOG
from qube.src.commons.utils import clean_nonserializable_attributes
from qube.src.services.kate4service import kate4Service

EMPTY = ''
get_details_params = [header_ex, path_ex, query_ex]
put_params = [header_ex, path_ex, body_put_ex]
delete_params = [header_ex, path_ex]
get_params = [header_ex]
post_params = [header_ex, body_post_ex]


class kate4ItemController(Resource):
    @swagger.doc(
        {
            'tags': ['kate4'],
            'description': 'kate4 get operation',
            'parameters': get_details_params,
            'responses': get_response_msgs
        }
    )
    @login_required
    def get(self, authcontext, entity_id):
        """gets an kate4 item that omar has changed
        """
        try:
            LOG.debug("Get details by id %s ", entity_id)
            data = kate4Service(authcontext['context'])\
                .find_by_id(entity_id)
            clean_nonserializable_attributes(data)
        except kate4ServiceError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': str(e.errors.value),
                                 'error_message': e.args[0]}), e.errors
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': '400',
                                 'error_message': e.args[0]}), 400
        return kate4Model(**data), 200

    @swagger.doc(
        {
            'tags': ['kate4'],
            'description': 'kate4 put operation',
            'parameters': put_params,
            'responses': put_response_msgs
        }
    )
    @login_required
    def put(self, authcontext, entity_id):
        """
        updates an kate4 item
        """
        try:
            model = kate4ModelPut(**request.get_json())
            context = authcontext['context']
            kate4Service(context).update(model, entity_id)
            return EMPTY, 204
        except kate4ServiceError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': str(e.errors.value),
                                 'error_message': e.args[0]}), e.errors
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': '400',
                                 'error_message': e.args[0]}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'error_code': '500',
                                 'error_message': ex.args[0]}), 500

    @swagger.doc(
        {
            'tags': ['kate4'],
            'description': 'kate4 delete operation',
            'parameters': delete_params,
            'responses': del_response_msgs
        }
    )
    @login_required
    def delete(self, authcontext, entity_id):
        """
        Delete kate4 item
        """
        try:
            kate4Service(authcontext['context']).delete(entity_id)
            return EMPTY, 204
        except kate4ServiceError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': str(e.errors.value),
                                 'error_message': e.args[0]}), e.errors
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': '400',
                                 'error_message': e.args[0]}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'error_code': '500',
                                 'error_message': ex.args[0]}), 500


class kate4Controller(Resource):
    @swagger.doc(
        {
            'tags': ['kate4'],
            'description': 'kate4 get operation',
            'parameters': get_params,
            'responses': get_response_msgs
        }
    )
    @login_required
    def get(self, authcontext):
        """
        gets all kate4 items
        """
        LOG.debug("Serving  Get all request")
        list = kate4Service(authcontext['context']).get_all()
        # normalize the name for 'id'
        return list, 200

    @swagger.doc(
        {
            'tags': ['kate4'],
            'description': 'kate4 create operation',
            'parameters': post_params,
            'responses': post_response_msgs
        }
    )
    @login_required
    def post(self, authcontext):
        """
        Adds a kate4 item.
        """
        try:
            model = kate4ModelPost(**request.get_json())
            result = kate4Service(authcontext['context'])\
                .save(model)

            response = kate4ModelPostResponse()
            for key in response.properties:
                response[key] = result[key]

            return (response, 201,
                    {'Location': request.path + '/' + str(response['id'])})
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': str(e.errors.value),
                                 'error_message': e.args[0]}), 400
        except ExtraValueException as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': '400',
                                 'error_message': "{} is not valid input".
                              format(e.args[0])}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'error_code': '500',
                                 'error_message': ex.args[0]}), 500
