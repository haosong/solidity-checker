contract KotET {
    address public king;
    uint public claimPrice = 100;
    address owner;
    function KotET() {
        owner = msg.sender; king = msg.sender;
    }
    function sweepCommission(uint amount) {
        owner.send(amount);
    }
    function () {
        if (msg.value < claimPrice) throw;
        uint compensation = calculateCompensation();
        king.send(compensation);
        king = msg.sender;
        claimPrice += calculateNewPrice();
        // change statevaible which occurs in if-statement will cause re-entry
    }
}
