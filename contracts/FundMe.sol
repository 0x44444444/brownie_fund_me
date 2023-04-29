// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    //OK, so a mapping is a hash table, all values point to something, if only the default value for the type in question

    mapping(address => uint256) public addToAmount;

    //An array of addresses
    //We will often need an array of keys for a hash table so we can loop over them and update the hash table
    //array plus mapping is a thing
    address[] public funders;
    //Create an owner address that we can use for 'require()' checks later on
    address public owner;
    //The Chainlink pricefeed contract, instantiated via an address passed into the constructor
    AggregatorV3Interface public priceFeed;

    //We set ownership of the contract in the constructor
    //Executed at the time of contract deployment
    constructor(address _priceFeed) public {
        //Set the pricefeed contract to be the one at the address we pass in
        priceFeed = AggregatorV3Interface(_priceFeed);
        //Set the owner variable to the address of the person who deploys the contract
        owner = msg.sender;
    }

    function fund() public payable {
        //So, 'payable' indicates that when calling the function,
        //an accompanying value of ETH can be sent with it
        //msg.sender is the address of the account calling the function
        //msg.value is the amount they sent with it
        //msg.value will be in wei anyway.
        uint256 minimumUSD = 50;
        //We need to adjust for 8 decimal precision stored as ints
        minimumUSD = minimumUSD * 10 ** 8;
        require(ethToUSD(msg.value) >= minimumUSD, "Minimum ETH not sent.");

        addToAmount[msg.sender] += msg.value;

        funders.push(msg.sender);
        //What is value of msg.value in USD?
    }

    function getVersion() public view returns (uint256) {
        //Type, Scope, Name
        //Scope not required as we're inside a function
        //So, we want to instantiate this interface, we know what type it is
        //But, we also need to know *where* it is (i.e. in terms of a contract address)
        //ChainLink maintain an address list at:
        //https://docs.chain.link/docs/ethereum-addresses/
        //This is the one for the Goerli testnet
        //AggregatorV3Interface clPriceFeed = AggregatorV3Interface(
        //    0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        //);
        //return clPriceFeed.version();
        return priceFeed.version();
    }

    function getDecimals() public view returns (uint8) {
        //AggregatorV3Interface clPriceFeed = AggregatorV3Interface(
        //    0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        //);

        //uint8 decimals = clPriceFeed.decimals();
        uint8 decimals = priceFeed.decimals();
        //We multiply up to get value in wei as by default it returns gwei value for 1 ETH
        //i.e.
        return decimals;
    }

    function getPrice() public view returns (uint256) {
        //AggregatorV3Interface clPriceFeed = AggregatorV3Interface(
        //    0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        //);
        //We need a tuple 'holder' to dump the return value into, we only want the second element
        //(, int256 answer, , , ) = clPriceFeed.latestRoundData();
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        //cast to uint256, not sure why
        //We multiply up to get value in wei as by default it returns gwei value for 1 ETH
        //i.e.
        //Returns the value of 1 ETH in USD to 8 decimal places using fixed point notation
        return uint256(answer);
    }

    function ethToUSD(uint256 ethAmount) public view returns (uint256) {
        //A function to convert a given amount of eth to its value in USD
        //This is going to be the current price of eth in wei, multipled by the wei amount of eth passed in

        uint256 ethPrice = getPrice();
        uint256 ethAmountinUSD = (ethPrice * ethAmount);
        //Our ethAmount is in wei, so we need to divide by 1*10^18
        return ethAmountinUSD / 1000000000000000000;
    }

    function getEntranceFee() public view returns (uint256) {
        //Returns what 50 USD in wei is, at the current price of Ethereum

        //First, we need to convert 50 bucks to fixed point 8 decimal places
        //To match what we get back from the oracle
        uint256 minimumUSD = 50 * 1e8;

        //Now grab what the oracle thinks 1 ETH is worth, fixed point, 8 decimal places
        uint256 price = getPrice();

        //If we just start dividing one by the other, the answer's going to be less than zero
        //i.e. 50 / 2000 = 0.025 ETH
        //Which will underflow into an int as 0
        //So... we want to work in wei anyway, so multiply the numerator by 1e18 prior to the division
        minimumUSD = minimumUSD * 1e18;
        //So, what we get back is the fee for 50
        return (minimumUSD / price);
    }

    //So, a modifier is like a little bit of function that one can apply to another function
    modifier onlyOwner() {
        require(msg.sender == owner);
        //The underscore is the marker where the rest of the function in question gets run from.
        //So, could in theory have it insert stuff before or after
        _;
    }

    //function (<parameter types>) {internal|external|public|private} [pure|constant|view|payable] [(modifiers)] [returns (<return types>)]

    function withdraw() public payable onlyOwner {
        //send to the person calling this function the balance contained in the contract with address of this
        //require(msg.sender == owner);
        msg.sender.transfer(address(this).balance);
        uint8 i;
        for (i = 0; i < funders.length; i++) {
            addToAmount[funders[i]] = 0;
        }
        //reset the funders array by declaring it to be a new, blank, array
        funders = new address[](0);
    }
}
