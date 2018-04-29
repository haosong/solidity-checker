# solidity-checker

## Install
````bash
npm install
````

## Usage
````bash
python3 main.py <*.sol>
````

## Features
Check 10 types of vulnerability as follows:

- Could potentially lead to re-entrancy vulnerability:
[link](http://solidity.readthedocs.io/en/develop/security-considerations.html#re-entrancy)

- Unchecked low-level call:
[link](https://consensys.github.io/smart-contract-best-practices/recommendations/#handle-errors-in-external-calls)

- Usage of send(), the recommended way is using transfer():
[link](http://solidity.readthedocs.io/en/develop/types.html#members-of-addresses)

- Usage of deprecated sha3(), the recommended way is using keccak256():
[link](https://github.com/ethereum/EIPs/issues/59)

- Usage of deprecated suicide(), the recommended way is using selfdestruct():
[link](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6.md)

- Usage of deprecated throw, the recommended way is using revert():
[link](https://solidity.readthedocs.io/en/develop/control-structures.html#error-handling-assert-require-revert-and-exceptions)

- Timestamp Dependence, such as using now() for randomness:
[link](https://consensys.github.io/smart-contract-best-practices/known_attacks/#timestamp-dependence)

- Could potentially lead overflow or underflow:
[link](https://ethereumdev.io/safemath-protect-overflows)

- No payable fallback function:
[link](http://solidity.readthedocs.io/en/develop/contracts.html#fallback-function)

- No return statement for function that returns value:
[link](https://tool.smartdec.net/knowledge/SOLIDITY_FUNCTIONS_RETURNS_TYPE_AND_NO_RETURN)


## Result of Example
````
$ python3 main.py simpledao.sol

13 warnings found!

================================ warning ================================

        address(dao).call.value(amount)(bytes4(sha3("donate(uint256)")),amount);
                                               ^-- Use keccak256() instead of sha3()
https://github.com/ethereum/EIPs/issues/59 

================================ warning ================================

        msg.sender.send(amount);
                   ^-- Use transfer() instead of send()
http://solidity.readthedocs.io/en/develop/types.html#members-of-addresses 

================================ warning ================================

                suicide(msg.sender);
                ^-- Use selfdestruct() instead of suicide()
https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6.md 

================================ warning ================================

                throw;
                ^-- Use revert() instead of throw
https://solidity.readthedocs.io/en/develop/control-structures.html#error-handling-assert-require-revert-and-exceptions 

================================ warning ================================

        address(dao).call.value(amount)(bytes4(sha3("donate(uint256)")),amount);
                     ^-- Low-level call() result unchecked
https://github.com/ConsenSys/smart-contract-best-practices#external-calls 

================================ warning ================================

        if (credit[msg.sender]>= amount) {
            if (!msg.sender.call.value(amount)()) {
                suicide(msg.sender);
                throw;
            }
            credit[msg.sender]-=amount;
--> Could potentially lead to re-entrancy vulnerability
http://solidity.readthedocs.io/en/develop/security-considerations.html#re-entrancy 

================================ warning ================================

        if (yourGuess == now % 2 > 0) {
                         ^-- Do not use now for randomness
https://github.com/ethereum/wiki/wiki/Safety#timestamp-dependence 

================================ warning ================================

    function queryCredit(address to) public returns (uint) {
        // return credit[to];
    }
--> No Return Statement
https://tool.smartdec.net/knowledge/SOLIDITY_FUNCTIONS_RETURNS_TYPE_AND_NO_RETURN 

================================ warning ================================

    function oddOrEven(bool yourGuess) external payable returns (bool) {

        // uint now = 1;

        if (yourGuess == now % 2 > 0) {
          uint fee = msg.value / 10;
          msg.sender.transfer(msg.value * 2 - fee);
        }
    }
--> No Return Statement
https://tool.smartdec.net/knowledge/SOLIDITY_FUNCTIONS_RETURNS_TYPE_AND_NO_RETURN 

================================ warning ================================

    function ()  {
        // dont receive ether via fallback
    }
--> Fallback function should have "payable" modifier.
http://solidity.readthedocs.io/en/develop/contracts.html#fallback-function 

================================ warning ================================

        uint d = b - a;
                 ^-- The subtraction operation might overflow
https://ethereumdev.io/safemath-protect-overflows/ 

================================ warning ================================

        uint c = a + b;
                 ^-- The addition operation might overflow
https://ethereumdev.io/safemath-protect-overflows/ 

================================ warning ================================

        uint e = a * b;
                 ^-- The multiplication operation might overflow
https://ethereumdev.io/safemath-protect-overflows/ 
````


