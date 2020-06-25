from loguru import logger

from app.models.chat import Chat
from app.models.user import User


async def create_super_user(user_id: int, remove: bool) -> bool:
    user = await User.query.where(User.id == user_id).gino.first()
    if not user:
        logger.error("User is not registered in bot")
        raise ValueError("User is not registered in bot")

    logger.info(
        "Loaded user {user}. It's registered at {register_date}.",
        user=user.id,
        register_date=user.created_at,
    )
    await user.update(is_superuser=not remove).apply()
    if remove:
        logger.warning("User {user} now IS NOT superuser", user=user_id)
    else:
        logger.warning("User {user} now IS superuser", user=user_id)
    return True


async def get_admin_chat():
    return await Chat.query.gino.first()


async def get_admin_user():
    return await User.query.where(User.is_superuser == True).gino.first()
