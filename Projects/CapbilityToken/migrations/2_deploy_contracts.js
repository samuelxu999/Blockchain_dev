var CapACToken = artifacts.require("./CapACToken.sol");
var RBACToken = artifacts.require("./RBACToken.sol");
var ABACToken = artifacts.require("./ABACToken.sol");

module.exports = function(deployer) {
	//deployer.deploy(CapACToken);
	//deployer.deploy(RBACToken);
	deployer.deploy(ABACToken);
};
