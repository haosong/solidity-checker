contract SimpleDAO {
    mapping (address => uint) public credit;
    
    function donate(uint amount) public {
        credit[msg.sender] += amount;
    }
    
    function queryCredit(address to) public returns (uint) {
        return credit[to];
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
}