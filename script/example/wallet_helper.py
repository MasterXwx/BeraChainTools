import asyncio
import os.path
from typing import Union

import aiofiles
from eth_account import Account
from eth_typing import Address, ChecksumAddress
from loguru import logger


# 从文件读取钱包的私钥，地址，助记词
def read_wallets_from_file(filename):
    accounts_list = []

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # 添加到列表中
            accounts_list.append(parse_line(line))

    return accounts_list


# 从文件中读取地址
def read_address_from_file(file_path):
    address_list = []
    if not os.path.exists(file_path):
        return address_list
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            address_list.append(line.strip())
    return address_list


# 解析生成钱包
def parse_line(line):
    # 分割每一行的内容
    parts = line.strip().split(', ')

    # 解析每个部分
    key = parts[0].split(': ')[1]
    address = parts[1].split(': ')[1]
    mnemonic = parts[2].split(': ')[1]
    return Wallet(key, address, mnemonic)


class Wallet(object):
    def __init__(self, private_key: str, address: str, mnemonic: str):
        self.private_key = private_key
        self.address = address
        self.mnemonic = mnemonic


# 单纯记录一个地址
async def record_address(file_path, address):
    async with aiofiles.open(file_path, 'a+') as f:
        await f.write(f'{address}\n')


# 把钱包记录到文件
async def write_to_file(key: str, address: Union[Address, ChecksumAddress], mnemonic: str):
    async with aiofiles.open(filePath, 'a+') as f:
        await f.write(f'Key: {key.hex()}, Address: {address}, Mnemonic: {mnemonic}\n')


# 读取记录的地址和余额
async def list_balance(file_path, address, balance):
    async with aiofiles.open(file_path, 'a+') as f:
        await f.write(f'address: {address}, balance: {balance}\n')


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


# 批量生成带助记词的钱包写入到 "./account/accounts.txt"
# 注意 append 为 True 为追加，否则只有在文件不存在的时候才能执行生效，不会有覆盖的操作
async def batch(append: bool, count):
    if (is_file_empty(filePath) or append):
        for _ in range(count):
            account_with_mnemonic = Account.create_with_mnemonic()
            account = account_with_mnemonic[0]
            mnemonic = account_with_mnemonic[1]
            key = account.key
            address = account.address

            # 异步地将信息写入文件
            await write_to_file(key, address, mnemonic)
    else:
        logger.debug('account already created ')


if __name__ == '__main__':
    filePath = "./account/accounts.txt"
    Account.enable_unaudited_hdwallet_features()
    # 使用 asyncio 运行异步主函数
    append = True
    asyncio.run(batch(append, 10))
