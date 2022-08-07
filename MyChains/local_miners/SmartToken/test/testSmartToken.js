const SmartToken = artifacts.require("SmartToken");

contract('SmartToken', (accounts) => {
	let SmartTokenInstance;
	let expected_coin;

	// make use of the before to provide initial setups
	before('deposit 100 value in the first account', async () => {
		SmartTokenInstance = await SmartToken.deployed();
		expected_coin = 100
		await SmartTokenInstance.depositToken(accounts[0],expected_coin, { from: accounts[0] })
	});
	it('should deposit 100 value in the first account', async () => {
		coin_balance = (await SmartTokenInstance.getTokens.call(accounts[0])).toNumber();
		assert.equal(coin_balance, expected_coin, "Owner should have depoist 100 coin");
	});
	
	// make use of the before to provide initial setups
	before('withdraw 90 value in the first account', async () => {
		await SmartTokenInstance.withdrawToken(accounts[0],90, { from: accounts[0] })
		expected_coin = 10
	});
	it('should withdraw 90 value from the first account', async () => {
		coin_balance = (await SmartTokenInstance.getTokens.call(accounts[0])).toNumber();
		assert.equal(coin_balance, expected_coin, "Owner should have depoist 100 coin");
	});
});