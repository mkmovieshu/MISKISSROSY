async def is_premium(user):
    return user.get("is_premium", False)
