import hashlib
import requests

import sys
import json
import time

def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while valid_proof(block_string, proof) is False:
        if proof % 10_000_000 is 0 and get_latest_block() == block:
            return -1
        proof += 1

    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] == '000000'

def get_latest_block():
    r = requests.get(url=node + "/last_block")
    try:
        data = r.json()
        return data
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)

if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coin_balance = 0

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        data = get_latest_block()

        # TODO: Get the block from `data` and use it to look for a new proof
        start_time = time.time()
        new_proof = proof_of_work(data['last_block'])
        total_time = time.time() - start_time

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        try:
            data = r.json()
        except ValueError:
            print("Error decoding value")
            print(r)

        if data['message'] == 'New block forged':
            coin_balance += 1
            print(f"A new block has been created in {total_time} seconds and you have received a coin.")
            print(f"Total balance: {coin_balance}")
        else:
            print('HOLY FUCK NO NO NO SHIT OH FUCK')
            print(data['message'])
        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it. Otherwise,
        # print the message from the server.
        
