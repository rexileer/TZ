from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message



class CheckSubscription(BaseMiddleware):
    
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
        ) -> Any:

        try:
            channel_member = await event.bot.get_chat_member("@anytechshop", event.from_user.id)
            if channel_member.status == "left":
                await event.answer("You should be subscribed to the channel @anytechshop.")
                return  
        except Exception as e:
            await event.answer("Failed to check channel subscription.")
            return  
        
        try:
            group_member = await event.bot.get_chat_member("@anytechchat", event.from_user.id)
            if group_member.status == "left":
                await event.answer("You need to be a member of the group @anytechchat.")
                return  
        except Exception as e:
            await event.answer("Failed to check group membership.")
            return 
        
        return await handler(event, data)