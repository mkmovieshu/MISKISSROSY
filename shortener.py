"""
Shortener Integration - Shortzy API support
Similar to TechVJ implementation
"""
import aiohttp
import logging
from vars import SHORTENER_URL, SHORTENER_API

logger = logging.getLogger(__name__)

try:
    from shortzy import Shortzy
except ImportError:
    Shortzy = None

async def get_short_link(original_link: str) -> str:
    """
    Original link ని short link లో convert చేయి
    Supports: shareus.io, shorturllink, terabox.in, urlshorten.in, etc.
    """
    
    if not SHORTENER_URL or not SHORTENER_API:
        return original_link  # No shortener configured
    
    # ShareUS special handling
    if SHORTENER_URL == "api.shareus.io":
        try:
            url = f'https://api.shareus.io/easy_api'
            params = {
                "key": SHORTENER_API,
                "link": original_link,
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    short_link = await response.text()
                    return short_link.strip()
        except Exception as e:
            logger.error(f"ShareUS shortener error: {e}")
            return original_link
    
    # Other shorteners using Shortzy
    elif Shortzy:
        try:
            shortzy = Shortzy(api_key=SHORTENER_API, base_site=SHORTENER_URL)
            short_link = await shortzy.convert(original_link)
            return short_link
        except Exception as e:
            logger.error(f"Shortzy error: {e}")
            return original_link
    
    return original_link

async def create_ad_short_link(bot_username: str, token: str) -> str:
    """
    Ad verification link create చేయ + short చేయి
    /start av_TOKEN -> short link
    """
    original_link = f"https://t.me/{bot_username}?start=av_{token}"
    short_link = await get_short_link(original_link)
    return short_link
