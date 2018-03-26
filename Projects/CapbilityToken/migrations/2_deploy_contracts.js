var CapACToken = artifacts.require("./CapACToken.sol");
var RBACToken = artifacts.require("./RBACToken.sol");

module.exports = function(deployer) {
	//deployer.deploy(CapACToken);
	deployer.deploy(RBACToken);
};
