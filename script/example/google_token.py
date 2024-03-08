import asyncio
from typing import Union

import aiohttp
from loguru import logger

# 打开下面的链接，注册生成自己的 client_key
client_key = 'https://yescaptcha.com/i/ZXbpaB'


async def get_yescaptcha_turnstile_token(session: aiohttp.ClientSession) -> Union[bool, str]:
    json_data = {"clientKey": client_key,
                 "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                          "websiteKey": "0x4AAAAAAARdAuciFArKhVwt",
                          "type": "TurnstileTaskProxylessM1"}, "softID": 109}
    async with session.post('https://cn.yescaptcha.com/createTask', json=json_data) as response:
        response_json = await response.json()
        if response_json['errorId'] != 0:
            logger.warning(response_json)
            return False
        task_id = response_json['taskId']
    for _ in range(120):
        data = {"clientKey": client_key, "taskId": task_id}
        async with session.post('https://cn.yescaptcha.com/getTaskResult', json=data) as response:
            response_json = await response.json()
            if response_json['status'] == 'ready':
                return response_json['solution']['token']
            else:
                await asyncio.sleep(3)
    return False
