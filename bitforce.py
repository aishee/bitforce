#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Infomation: Script to brute bitcoin

from bit import Key
import os
import json
import time
import ecdsa
import hashlib
import requests
import binascii


class pau:
    pau = 0


def prikey():
    return binascii.hexlify(os.urandom(32)).decode('utf-8')


def pubkey(prikey):
    prikey = binascii.unhexlify(prikey)
    sign = ecdsa.SigningKey.from_string(prikey, curve=ecdsa.SECP256k1)
    return '04' + binascii.hexlify(
        sign.verifying_key.to_string()).decode('utf-8')


def address(pubkey):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    ares = '0'
    byte = '00'
    zero = 0
    val = hashlib.new('ripemd160')
    val.update(hashlib.sha256(binascii.unhexlify(pubkey.encode())).digest())
    cim = (byte + val.hexdigest())
    doublehash = hashlib.sha256(
        hashlib.sha256(binascii.unhexlify(cim.encode())).digest()).hexdigest()
    address = cim + doublehash[0:8]
    for char in address:
        if (char != ares):
            break
        zero += 1
    zero = zero // 2
    nom = int(address, 16)
    result = []
    while (nom > 0):
        nom, reder = divmod(nom, 58)
        result.append(alphabet[reder])
    count = 0
    while (count < zero):
        result.append(alphabet[0])
        count += 1
    return ''.join(result[::-1])


def balance(address):
    APIGet = requests.get(
        "http://webbtc.com/address/" + str(address) + ".json")
    if (APIGet.status_code == 429):
        pau.pau += 1
        if (pau.pau >= 10):
            print("\nUnable to connect to API\nRetrying in 10 seconds\n")
            time.sleep(30)
            pau.pau = 0
        return -1
    if (APIGet.status_code != 200 and APIGet.status_code != 404
            and APIGet.status != 429):
        print("\nHTTP Error Code: " + str(APIGet.status_code) +
              "\nRetrying in 10 seconds\n")
        time.sleep(10)
        return -1
    data = APIGet.json()
    balance = int(data["balance"])
    pau.pau = 0
    return balance


def main():
    data = [0, 0, 0, 0]
    while True:
        data[0] = prikey()
        data[1] = pubkey(data[0])
        data[2] = address(data[1])
        data[3] = balance(data[2])
        datas = (
            "\nAddress: " + str(data[2]) + "\n" + "Private Key: " +
            str(data[0]) + "\n" + "Wallet Import Format Private Key: " +
            str(Key.from_hex(data[0]).to_wif()) + "\n" + "Public Key: " + str(
                data[1]).upper() + "\n" + "Balance: " + str(data[3]) + "\n")
        if (data[3] == -1):
            continue
        if (data[3] == 0):
            print("{:34}".format(str(data[2])) + " = " + str(data[3]))
        if (data[3] > 0):
            print(datas)
            fl = open("bitforce-found.txt", "a")
            fl.write(datas)
            fl.close()


if __name__ == '__main__':
    print("\n-----------------Warning Wallet Balance---------------!")
    main()
