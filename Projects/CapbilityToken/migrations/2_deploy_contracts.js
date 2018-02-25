var CapACToken = artifacts.require("./CapACToken.sol");

module.exports = function(deployer) {
	deployer.deploy(CapACToken);
};
