import { Conflux } from 'js-conflux-sdk';
import GameItem from './deploys/GameItem.json' assert {type: 'json'};
import ERC721 from './deploys/ERC721.json' assert {type: 'json'};
export {invoke}


const abi = GameItem.abi
const address = GameItem.receipt.contractCreated

const cfx = new Conflux({
    url: 'http://test.confluxrpc.org',
    networkId: 1,
});


function invoke(playerAddress, tokenURI){
    // 建立合约
    const nftContract = cfx.Contract({
        abi, address
    })
    // 调用awardItem函数
    const newItemId = nftContract.awardItem(playerAddress, tokenURI);
    console.log(newItemId);
}

// console.log(contractData);

// const playerAddress = 'cfxtest:aathvsw97m8td0ref0fp5fkzfc0wsrzu0am1k0519x';
// const tokenURI = 'https://ipfs.io/ipfs/Qmd7uVCXavzXx3sQRzigZsaAQjWa36XnZWhimBwmm7NXC5';
// invoke(playerAddress, tokenURI);
