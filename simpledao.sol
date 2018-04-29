contract SimpleDAO {
    mapping (address => uint) public credit;
    
    function donate(uint amount) public {
        credit[msg.sender] += amount;
    }
    
    function queryCredit(address to) public returns (uint) {
        // return credit[to];
    }
    
    function donateToSimpleDAO(uint amount) public {
        address(dao).call.value(amount)(bytes4(sha3("donate(uint256)")),amount);
    }

    function withdraw(uint amount) public {
        msg.sender.send(amount);
        if (credit[msg.sender]>= amount) {
            if (!msg.sender.call.value(amount)()) {
                throw;
            }
            credit[msg.sender]-=amount;
        }
    }
    
    function checkBalance() public returns (uint) {
        return address(this).balance;
    }

    function oddOrEven(bool yourGuess) external payable returns (bool) {

        // uint now = 1;

        if (yourGuess == now % 2 > 0) {
          uint fee = msg.value / 10;
          msg.sender.transfer(msg.value * 2 - fee);
        }
    }

    function ()  {
        // dont receive ether via fallback
    }

}