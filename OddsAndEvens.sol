contract OddsAndEvens{
	struct Player { address addr; uint number;}
	Player[2] private players;
	uint8 tot = 0; address owner;

	function OddsAndEvens() {owner = msg.sender;}

	function play(uint number) {
		if (msg.value != 1 ether) throw;
		players[tot] = Player(msg.sender, number);
		tot++;
		if (tot==2) andTheWinnerIs();
	}
	function andTheWinnerIs() private {
		uint n = players[0].number + players[1].number;
		players[n%2].addr.send(1800 finney);
		delete players;
		tot=0;
	}

	function getProfit() {
		owner.send(this.balance);
	}
}
