contract test {
  function send() {
    // address(dao).call.value(amount)(bytes4(sha3("withdraw(uint256)")),amount);  
    dao.call.value();
  }
}

