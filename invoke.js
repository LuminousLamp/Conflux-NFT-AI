// import { Conflux } from 'js-conflux-sdk';
const Conflux = require('js-conflux-sdk')
// import GameItem from './deploys/GameItem.json' assert {type: 'json'};
// import ERC721 from './deploys/ERC721.json' assert {type: 'json'};
// export {invoke}


// const abi = GameItem.abi
// const address = GameItem.receipt.contractCreated
const abi =  [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor",
      "name": "constructor"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "owner",
          "type": "address",
          "networkId": 1
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "approved",
          "type": "address",
          "networkId": 1
        },
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "Approval",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "owner",
          "type": "address",
          "networkId": 1
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "operator",
          "type": "address",
          "networkId": 1
        },
        {
          "indexed": false,
          "internalType": "bool",
          "name": "approved",
          "type": "bool"
        }
      ],
      "name": "ApprovalForAll",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "from",
          "type": "address",
          "networkId": 1
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "to",
          "type": "address",
          "networkId": 1
        },
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "Transfer",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "to",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "approve",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "owner",
          "type": "address",
          "networkId": 1
        }
      ],
      "name": "balanceOf",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "getApproved",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address",
          "networkId": 1
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "owner",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "address",
          "name": "operator",
          "type": "address",
          "networkId": 1
        }
      ],
      "name": "isApprovedForAll",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "name",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "ownerOf",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address",
          "networkId": 1
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "safeTransferFrom",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        },
        {
          "internalType": "bytes",
          "name": "_data",
          "type": "bytes"
        }
      ],
      "name": "safeTransferFrom",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "operator",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "bool",
          "name": "approved",
          "type": "bool"
        }
      ],
      "name": "setApprovalForAll",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes4",
          "name": "interfaceId",
          "type": "bytes4"
        }
      ],
      "name": "supportsInterface",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "symbol",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "tokenURI",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "transferFrom",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "player",
          "type": "address",
          "networkId": 1
        },
        {
          "internalType": "string",
          "name": "tokenURI",
          "type": "string"
        }
      ],
      "name": "awardItem",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]

const address = "cfxtest:acgp8t8kawk1t7fjae92bkr2tc6w8vavzayg762z7d"
const cfx = new Conflux.Conflux({
    url: 'http://test.confluxrpc.org',
    networkId: 1,
});


async function invoke(playerAddress, tokenURI){
    // 建立合约
    const nftContract = cfx.Contract({
        abi:abi, address:address
    })

    console.log('balance of me: '+nftContract.balanceOf(playerAddress));
    console.log('name: '+nftContract.name());
    console.log('owner of 2: '+nftContract.ownerOf(2));
    
    // 调用awardItem函数
    const newItemId = nftContract.awardItem(playerAddress, tokenURI);
    console.log(newItemId);
}

// console.log(contractData);

const playerAddress = 'cfxtest:aathvsw97m8td0ref0fp5fkzfc0wsrzu0am1k0519x';
const tokenURI = 'https://ipfs.io/ipfs/Qmd7uVCXavzXx3sQRzigZsaAQjWa36XnZWhimBwmm7NXC5';
invoke(playerAddress, tokenURI);
