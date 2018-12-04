# -*- coding: utf-8 -*-
'''
------------------------------------------------------------
File Name: login_async.py
Description : 
Project: Spiders
Last Modified: Monday, 19th November 2018 3:07:26 pm
-------------------------------------------------------------
'''

from pathlib import Path
import time
import urllib.parse
import json

import aiohttp
from aiohttp import ClientSession
import execjs
import aiofiles

js_path = Path(__file__).absolute().parent/"encrypt.js"
with open(js_path, encoding='utf-8') as f:
    jsdata = f.read()
jsdata = execjs.compile(jsdata)


def get_analysis(url: str, params: str = "{}", full: bool=False) -> str:
    analysis = jsdata.call('get_analysis', url, params)
    if not full:
        analysis = json.loads(analysis).get('analysis')
    return analysis


async def if_need_login(session):
    params = {
        "analysis": get_analysis(url="https://api.qimai.cn/account/userinfo")
    }
    response = await session.get(url="https://api.qimai.cn/account/userinfo", params=params)
    if not (await response.json())["userinfo"]["username"]:
        return True
    else:
        print(1)
        return False


async def qimai_login_async(username: str = "17123547402", password: str = "linhanqiu1123.") -> ClientSession:
    headers = {
        'Referer': 'https://www.qimai.cn/rank',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    cookies = aiohttp.CookieJar()
    cookie_path = Path(__file__).absolute().parent/f"cookies_{username}"
    if cookie_path.exists():
        cookies.load(cookie_path)
    Session = aiohttp.ClientSession(
        headers=headers, cookie_jar=cookies)
    if not await if_need_login(session=Session):
        return Session
    # step_1
    url = 'https://www.qimai.cn/account/signin/r/%2F'
    response = await Session.get(url)
    # step_2
    url = 'https://api.qimai.cn/account/pageCheck/type/signin'
    full_url = f'https://api.qimai.cn/account/pageCheck/type/signin?analysis={urllib.parse.quote(get_analysis(url=url))}'
    response = await Session.get(url)
    print(await response.text())
    # step_3
    url = 'https://api.qimai.cn/account/userinfo'
    full_url = f'https://api.qimai.cn/account/userinfo?analysis={urllib.parse.quote(get_analysis(url=url))}'
    response = await Session.get(url)
    print(await response.text())
    # step_4
    url = 'https://api.qimai.cn/index/index'
    full_url = f'https://api.qimai.cn/index/index?analysis={urllib.parse.quote(get_analysis(url=url))}'
    response = await Session.get(url)
    print(await response.text())
    # step_5
    url = f'https://api.qimai.cn/account/getVerifyCodeImage?{str(int(time.time() * 1000))}'
    response = await Session.get(url)
    async with aiofiles.open(f'captcha_{username}.jpg', 'wb') as f:
        await f.write(await response.read())
    # step_6
    captcha = input('input code:')
    url = 'https://api.qimai.cn/account/signinForm'
    login_url = f'https://api.qimai.cn/account/signinForm?analysis={urllib.parse.quote(get_analysis(url=url))}'
    data = {
        'username': username,
        'password': password,
        'code': captcha,  # 验证码
    }
    response = await Session.post(login_url, data=data)
    data = await response.json()
    if data.get('msg') == '登录成功':
        print('登录成功!用户名为:' + data.get('userinfo').get('username'))
        # USERINFO 就是登录成功返回的cookie
        await write_session(session=Session, cookie_path=cookie_path)
        return Session
    elif data.get('msg') == '验证码错误，请重试':
        print('验证码错误，请重试!')
        return None
    elif data.get('msg') == '用户名或密码错误':
        print('用户名或密码错误')
        return None


async def write_session(session: object, cookie_path: Path):
    session.cookie_jar.save(cookie_path)
