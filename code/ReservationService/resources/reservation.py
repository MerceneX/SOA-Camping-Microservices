from flask import Response, request
from flask_restful_swagger_3 import Resource, swagger
from database.models.reservation import Reservation

from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, DataAlreadyExistsError, InternalServerError, UpdatingDataError, \
    DeletingDataError, DataNotExistsError


class ReservationsApi(Resource):
    @swagger.tags(['Reservations'])
    @swagger.response(response_code=200, description="List of reservations")
    def get(self):
        reservations = Reservation.objects().to_json()
        return Response(reservations, mimetype="application/json", status=200)

    @swagger.tags(['Reservations'])
    @swagger.response(response_code=201, description="Create new reservation")
    def post(self):
        try:
            body = request.get_json()
            reservation = Reservation(**body).save()
            id = reservation.id
            return {'reservation_id': str(id)}, 201
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise DataAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class ReservationApi(Resource):
    @swagger.tags(['Reservations'])
    @swagger.response(response_code=204, description="No content")
    def put(self, reservation_id):
        try:
            body = request.get_json()
            Reservation.objects.get(id=reservation_id).update(**body)
            return '', 204
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingDataError
        except Exception:
            raise InternalServerError

    @swagger.tags(['Reservations'])
    @swagger.response(response_code=204, description="No content")
    def delete(self, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id).delete()
            return '', 204
        except DoesNotExist:
            raise DeletingDataError
        except Exception:
            raise InternalServerError

    @swagger.tags(['Reservations'])
    @swagger.response(response_code=200, description="One reservation")
    def get(self, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id).to_json()
            return Response(reservation, mimetype="application/json", status=200)
        except DoesNotExist:
            raise DataNotExistsError
        except Exception:
            raise InternalServerError