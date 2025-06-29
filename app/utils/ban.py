import asyncio
import json
import logging
import httpx

from app.config import CF_TOKEN

logger = logging.getLogger(__name__)


async def verify_cloudflare():
    token = CF_TOKEN
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/d3bb93d613eeb730d41d8d4f57b2f903/tokens/verify"
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        logger.info(f'Cloudflare verified')
        return id
    except httpx.HTTPStatusError:
        message = f"[{response.status_code}] {response.text}"
        logger.error(message)
    except Exception as error:
        message = f"An unexpected error occurred: {error}"
        logger.error(message)


async def ban_ip_with_timeout(ip: str, seconds: int):
    id = await ban_ip(ip, seconds)

    await asyncio.sleep(seconds)

    await unban_ip_with_id(id)


async def ban_ip(ip: str, seconds: int):
    token = CF_TOKEN
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "mode": "block",
        "configuration": {
            "target": "ip",
            "value": ip
        },
        "notes": "Temp block for 30 seconds"
    }
    url = f"https://api.cloudflare.com/client/v4/user/firewall/access_rules/rules"
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers, data=json.dumps(payload), timeout=10)
            response.raise_for_status()
        json_obj = response.json()
        id = json_obj["result"]["id"]
        logger.info(f'Ip {ip} banned for {seconds} seconds with role id {id}')
        return id
    except httpx.HTTPStatusError:
        message = f"[{response.status_code}] {response.text}"
        logger.error(message)
    except Exception as error:
        message = f"An unexpected error occurred: {error}"
        logger.error(message)


async def unban_ip_with_id(id: str):
    token = CF_TOKEN
    headers = {
        "Authorization": f"Bearer {token}",
    }
    url = f"https://api.cloudflare.com/client/v4/user/firewall/access_rules/rules/{id}"
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.delete(url, headers=headers, timeout=10)
            response.raise_for_status()
        logger.info(f'Role id with {id} unbanned')
        return id
    except httpx.HTTPStatusError:
        message = f"[{response.status_code}] {response.text}"
        logger.error(message)
    except Exception as error:
        message = f"An unexpected error occurred: {error}"
        logger.error(message)


async def unban_ip(ip: str):
    token = CF_TOKEN
    headers = {
        "Authorization": f"Bearer {token}",
    }
    url = f"https://api.cloudflare.com/client/v4/user/firewall/access_rules/rules"
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        json_obj = response.json()
        id = next(
            (r for r in json_obj["result"] if r['configuration']['value'] == ip), None)["id"]
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.delete(url+f'/{id}', headers=headers, timeout=10)
            response.raise_for_status()
        logger.info(f'Role id with {id} unbanned')
        return id
    except httpx.HTTPStatusError:
        message = f"[{response.status_code}] {response.text}"
        logger.error(message)
    except Exception as error:
        message = f"An unexpected error occurred: {error}"
        logger.error(message)

async def unban_all():
    token = CF_TOKEN
    headers = {
        "Authorization": f"Bearer {token}",
    }
    url = f"https://api.cloudflare.com/client/v4/user/firewall/access_rules/rules"
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        json_obj = response.json()
        for r in json_obj["result"]:
            id=r['id']
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.delete(url+f'/{id}', headers=headers, timeout=10)
                response.raise_for_status()
        logger.info(f'All ips unbanned')
        return id
    except httpx.HTTPStatusError:
        message = f"[{response.status_code}] {response.text}"
        logger.error(message)
    except Exception as error:
        message = f"An unexpected error occurred: {error}"
        logger.error(message)
