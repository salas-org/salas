// TODO: need to specify a license 
// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.7;

contract Salas {

    // Declare state variables of the contract
    address private _owner;
    uint256 private _cost_in_wei;

    // // // // // // // // // // // 
    // EVENTS
    // // // // // // // // // // // 

    // This is the event that makes the log, in which the miners will search
    event RegisteredAddress(address indexed senderAddress, string id_chain, string public_key_certificate, string signed_address);
    event OwnershipTransferred(address previousOwner, address newOwner);

    // // // // // // // // // // // 
    // CONSTRUCTORS & MODIFIERS
    // // // // // // // // // // // 

    // Constructor
    constructor() {
        _owner = msg.sender;
        _cost_in_wei = 2_000_000;  //TODO: add some appropriate cost: should cost too much to DOS, should be little so everyone can pay it 
    }

    // Modifier
    modifier onlyOwner() {
        require(_owner == msg.sender, "caller is not the owner");
        _;
    }

    // // // // // // // // // // // 
    // PUBLIC
    // // // // // // // // // // // 

    function registerAddress(string calldata id_chain, string calldata public_key_certificate, string calldata signed_address) payable external {
        // msg.sender is the address to be registered
        // id_chain is the number used to verify the public key (identifies a certificate authority chain) 
        // public_key is the public key of the private key used to sign the address below
        // signed_address == id_sign(msg.sender)
        
        // TODO: check the input values for max length 

        require(msg.value >= _cost_in_wei, "You must pay at least cost ETH");

        // emit the event so the log is permanently stored
        emit RegisteredAddress(msg.sender, id_chain, public_key_certificate, signed_address);
    }

    function getCost() external view returns(uint) {
        return _cost_in_wei;
    }

    // // // // // // // // // // // 
    // OWNER ONLY
    // // // // // // // // // // // 

    function setCost(uint amount) external onlyOwner {
        _cost_in_wei = amount;
    }

    // allow to withdraw the eth in the contract
    function withdraw(uint amount) external onlyOwner returns(uint){
        require(amount < address(this).balance, "Insufficient balance");
        payable(_owner).transfer(amount);
        return amount;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != _owner);
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }    
}
