from functools import wraps

from sanic import Blueprint, response
from sanic.response import json

from src.exceptions import InvalidAuthorizationTokenException
from src.utils import expects_json_object

blueprint = Blueprint("root", version="v1")


def auth_required(f):
    @wraps(f)
    async def decorated_function(request, *args, **kwargs):
        PREFIX = "Bearer "
        header = request.headers.get("Authorization")
        if header is None or not header.startswith(PREFIX):
            raise InvalidAuthorizationTokenException("Invalid Authorization Bearer")
        token = header[len(PREFIX):]
        linkedin_user = request.app.linkedin_login.get_linkedin_user(token=token)
        user = request.app.user_service.get_user_by_linkedin_id(
            user_id=linkedin_user.get("user_id")
        )
        if user is None:
            raise ResourceNotOwnedException("User not found")

        response = await f(request, user, *args, **kwargs)
        return response

    return decorated_function


@blueprint.get("/auth/me")
@auth_required
async def user_info(request, user):
    user = request.app.user_service.get_user_by_linkedin_id(user_id=user.get("user_id"))
    return json({"me": user})


@blueprint.get("/")
async def root(request):
    return json({"hello": "world"})


@blueprint.post("/user/")
@expects_json_object
async def create_user(request):
    user = request.app.user_service.create_if_not_exists(**request.json)
    return json(user)


@blueprint.get("/sell_order/")
@auth_required
async def get_sell_orders_by_user(request, user):
    return json(request.app.sell_order_service.get_orders_by_user(user_id=user["id"]))


@blueprint.get("/sell_order/<id>")
@auth_required
async def get_sell_order_by_id(request, user, id):
    return json(
        request.app.sell_order_service.get_order_by_id(id=id, user_id=user["id"])
    )


@blueprint.post("/sell_order/")
@auth_required
@expects_json_object
async def create_sell_order(request, user):
    return json(
        request.app.sell_order_service.create_order(
            **request.json, user_id=user["id"], scheduler=request.app.scheduler
        )
    )


@blueprint.patch("/sell_order/<id>")
@auth_required
@expects_json_object
async def edit_sell_order(request, user, id):
    return json(
        request.app.sell_order_service.edit_order(
            **request.json, id=id, subject_id=user["id"]
        )
    )


@blueprint.delete("/sell_order/<id>")
@auth_required
async def delete_sell_order(request, user, id):
    return json(
        request.app.sell_order_service.delete_order(id=id, subject_id=user["id"])
    )


@blueprint.get("/buy_order/")
@auth_required
async def get_buy_orders_by_user(request, user):
    return json(request.app.buy_order_service.get_orders_by_user(user_id=user["id"]))


@blueprint.get("/buy_order/<id>")
@auth_required
async def get_buy_order_by_id(request, user, id):
    return json(
        request.app.buy_order_service.get_order_by_id(id=id, user_id=user["id"])
    )


@blueprint.post("/buy_order/")
@auth_required
@expects_json_object
async def create_buy_order(request, user):
    return json(
        request.app.buy_order_service.create_order(**request.json, user_id=user["id"])
    )


@blueprint.patch("/buy_order/<id>")
@auth_required
@expects_json_object
async def edit_buy_order(request, user, id):
    return json(
        request.app.buy_order_service.edit_order(
            **request.json, id=id, subject_id=user["id"]
        )
    )


@blueprint.delete("/buy_order/<id>")
@auth_required
async def delete_buy_order(request, user, id):
    return json(
        request.app.buy_order_service.delete_order(id=id, subject_id=user["id"])
    )


@blueprint.get("/security/")
async def get_all_securities(request):
    return json(request.app.security_service.get_all())


@blueprint.patch("/security/<id>")
@auth_required
async def edit_security_market_price(request, user, id):
    return json(
        request.app.edit_market_price(**request.json, id=id, subject_id=user["id"])
    )


@blueprint.get("/round/")
async def get_all_rounds(request):
    return json(request.app.round_service.get_all())


@blueprint.get("/round/active")
async def get_active_round(request):
    return json(request.app.round_service.get_active())


@blueprint.get("/round/previous/statistics/<security_id>")
async def get_active_round(request, security_id):
    return json(
        request.app.round_service.get_previous_round_statistics(security_id=security_id)
    )


@blueprint.post("/ban/")
@auth_required
@expects_json_object
async def ban_user(request, user):
    return json(
        request.app.banned_pair_service.ban_user(**request.json, my_user_id=user["id"])
    )


@blueprint.get("/linkedin/auth/buyer")
async def linkedin_auth_buyer(request):
    socket_id = request.args.get("socketId")
    url = request.app.linkedin_login.get_auth_url(socket_id, is_buy=True)
    return response.redirect(url)


@blueprint.get("/linkedin/auth/seller")
async def linkedin_auth_seller(request):
    socket_id = request.args.get("socketId")
    url = request.app.linkedin_login.get_auth_url(socket_id, is_buy=False)
    return response.redirect(url)


@blueprint.get("/linkedin/auth/callback/buyer")
async def linkedin_auth_callback_buyer(request):
    code = request.args.get("code")
    state = request.args.get("state")
    return json(request.app.linkedin_login.authenticate(code=code, socket_id=state, is_buy=True))


@blueprint.get("/linkedin/auth/callback/seller")
async def linkedin_auth_callback_seller(request):
    code = request.args.get("code")
    state = request.args.get("state")
    return json(request.app.linkedin_login.authenticate(code=code, socket_id=state, is_buy=False))


@blueprint.get("/requests/buy/")
@auth_required
async def get_buy_requests(request, user):
    return json(
        request.app.user_request_service.get_buy_requests(subject_id=user["id"])
    )


@blueprint.get("/requests/sell/")
@auth_required
async def get_sell_requests(request, user):
    return json(
        request.app.user_request_service.get_sell_requests(subject_id=user["id"])
    )


@blueprint.post("/requests/<id>")
@auth_required
async def approve_request(request, id, user):
    return json(
        request.app.user_request_service.approve_request(
            request_id=id, subject_id=user["id"]
        )
    )


@blueprint.delete("/requests/<id>")
@auth_required
async def reject_request(request, id, user):
    return json(
        request.app.user_request_service.reject_request(
            request_id=id, subject_id=user["id"]
        )
    )
