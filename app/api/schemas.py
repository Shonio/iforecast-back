from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=3))


class MeteoDayStatsSchema(Schema):
    power_plant_id = fields.Int(required=True)
    timestamp = fields.Date(required=True, format="%Y-%m-%d")


class PowerPlantDayStatsSchema(Schema):
    power_plant_id = fields.Int(required=True)
    timestamp = fields.Date(required=True, format="%Y-%m-%d")


class PowerPlantMonthStatsSchema(Schema):
    power_plant_id = fields.Int(required=True)
    timestamp = fields.Date(required=True, format="%Y-%m")


class PowerPlantYearStatsSchema(Schema):
    power_plant_id = fields.Int(required=True)
    timestamp = fields.Date(required=True, format="%Y")


class TeamMemberSchema(Schema):
    full_name = fields.Str(required=True, validate=[validate.Length(min=1)])
    position = fields.Str(
        required=True,
        validate=validate.OneOf(["Director", "Engineer", "Operator", "Dispatcher"]),
    )
    phone = fields.Int(required=True)


class TeamMemberUpdateSchema(Schema):
    id = fields.Int(required=True)
    full_name = fields.Str(required=True, validate=[validate.Length(min=1)])
    position = fields.Str(
        required=True,
        validate=validate.OneOf(["Director", "Engineer", "Operator", "Dispatcher"]),
    )
    phone = fields.Int(required=True)


class ChangeEmailSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=3))


class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True, validate=validate.Length(min=3))
    new_password = fields.Str(required=True, validate=validate.Length(min=3))
