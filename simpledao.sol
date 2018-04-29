contract SimpleDAO {
    mapping (address => uint) public credit;
    
    function donate(uint amount) public {
        credit[msg.sender] += amount;
    }
    
    function queryCredit(address to) public returns (uint) {
        // return credit[to];
    }
    
     function withdraw(uint amount) public {
        if (credit[msg.sender]>= amount) {
            msg.sender.call.value(amount)();
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