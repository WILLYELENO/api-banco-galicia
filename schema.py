from marshmallow import fields, Schema


class SimulatorSchema (Schema):
    cuit_list = fields.List(
        cls_or_instance=fields.String,
        required=True,
        load_only=True
    )


class FilterSchema (Schema):

    name_loan = fields.String(required=False,load_default=None)
    interest_rate = fields.String(required=False,load_default=None)
    name_person = fields.String(required=False,load_default=None)
    cuit = fields.String(required=False,load_default=None)


class FindLoansSchema (Schema):
    id_loan_model = fields.String(dump_only=True)
    name_loan = fields.String()
    interes_rate = fields.String()
    name_person = fields.String()
    cuit = fields.String()
    create_date = fields.String()