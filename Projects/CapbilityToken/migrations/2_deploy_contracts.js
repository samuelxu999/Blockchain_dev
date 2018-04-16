var CapACToken = artifacts.require("./CapACToken.sol");
var RBACToken = artifacts.require("./RBACToken.sol");
var ABACToken = artifacts.require("./ABACToken.sol");
var DelegateToken = artifacts.require("./DelegateToken.sol");

module.exports = function(deployer) {
	//deployer.deploy(CapACToken);
	//deployer.deploy(RBACToken);
	//deployer.deploy(ABACToken);
	deployer.deploy(DelegateToken);
};
