// SPDX-License-Identifier: MIT
pragma solidity >=0.4.18;

// These files are dynamically created at test time
import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/SmartToken.sol";

contract TestSmartToken {

  function test_depositTokenUsingDeployedContract() public {
    SmartToken token = SmartToken(DeployedAddresses.SmartToken());

    uint expected_coin = 100;
    address expected_owner = tx.origin;

    // deposit 100 to initial account
    token.depositToken(expected_owner,expected_coin);

    Assert.equal(token.getTokens(expected_owner), expected_coin, "Owner should have depoist 100 coin");
  }

  function test_withdrawTokenUsingDeployedContract() public {
    SmartToken token = SmartToken(DeployedAddresses.SmartToken());

    uint expected_coin = 90;
    address expected_owner = tx.origin;

    // withdraw 10 from existing balance: 100
    token.withdrawToken(expected_owner,10);

    Assert.equal(token.getTokens(expected_owner), expected_coin, "Owner should have withdraw 100 coin");
  }

  function test_depositToken() public {
    SmartToken token = new SmartToken();

    uint expected_coin = 100;
    address expected_owner = address(this);

    // deposit balance 100
    token.depositToken(expected_owner,expected_coin);

    Assert.equal(token.getTokens(expected_owner), expected_coin, "Owner should have depoist 100 coin");
  }

  function test_withdrawToken() public {
    SmartToken token = new SmartToken();

    uint expected_coin = 10;
    address expected_owner = address(this);

    // initialize balance 100
    token.depositToken(expected_owner,110);

    token.withdrawToken(expected_owner,100);

    Assert.equal(token.getTokens(expected_owner), expected_coin, "Owner should have withdraw 100 coin");
  }

}
