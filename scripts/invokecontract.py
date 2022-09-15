
import json, os
import conflux_web3.exceptions
from conflux_web3 import Web3

def invoke(playerAddress, tokenURI):

    web3 = Web3(Web3.HTTPProvider("https://test.confluxrpc.com"))

    # with open('..\\build\\contracts\\GameItem.json','r') as fp:
    with open('..\\deploys\\GameItem.json','r')as fp:
        contract_metadata = json.load(fp)

    nftContract = web3.cfx.contract(
        abi=contract_metadata["abi"], 
        address=contract_metadata["receipt"]["contractCreated"]
        )
    random_account = web3.account.create()
    newItemId = nftContract.caller().awardItem(playerAddress, tokenURI)
    print(newItemId)


# conflux_web3.exceptions.DisabledException

# playerAddress = 'cfxtest:aathvsw97m8td0ref0fp5fkzfc0wsrzu0am1k0519x'
# tokenURI = 'https://ipfs.io/ipfs/QmV1SUM2nVATy4J4qLhJP97hguQiT5iJCgvcm8B7Cgb1Kf'
# invoke(playerAddress,tokenURI)

# you might need to change the argument name depending on the solidity source code
# below works if wallet middleware and default account is set 
# see examples/10-send_raw_transactions.py if you want to manually sign and send transactions
# hash = nftContract.constructor(name="ERC20", symbol="C", initialSupply=10**18).transact()
# or use 
# contract_address = hash.executed()["contractCreated"]
# contract_address = web3.cfx.wait_for_transaction_receipt(hash)["contractCreated"] 
# assert contract_address is not None
# print(f"contract deployed: {contract_address}")
# print()

# contract = web3.cfx.contract(contract_address, abi=contract_metadata["abi"])
# random_account = web3.account.create()


# contract.functions.transfer(random_account.address, 100) prebuilt the transaction
# the transaction is not send until .transact() is called
# prebuilt_tx = contract.functions.transfer(random_account.address, 100)
# hash = prebuilt_tx.transact()
# transfer_receipt = web3.cfx.wait_for_transaction_receipt(hash)

# # 2 ways to call, either is ok
# balance = contract.functions.balanceOf(random_account.address).call()
# balance1 = contract.caller().balanceOf(random_account.address)
# assert balance1 == balance == 100
# print("transfer success")
# print()

# parameter definitions: https://developer.confluxnetwork.org/conflux-doc/docs/json_rpc#cfx_getlogs
# fromEpoch = transfer_receipt["epochNumber"]
# logs = web3.cfx.get_logs(fromEpoch=fromEpoch, address=contract_address)
# print("raw logs: ")
# print(logs)
# print()