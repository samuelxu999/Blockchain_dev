pragma solidity >=0.4.18;        

contract SmartToken {
        mapping(address => uint) tokens;

        event OnValueChanged(address indexed _from, uint _value);

        function depositToken(address recipiant, uint value) public returns (bool success) {
                tokens[recipiant] += value;
                emit OnValueChanged(recipiant, tokens[recipiant]);
                return true;
        }
        function withdrawToken(address recipiant, uint value) public returns (bool success) {
                if((tokens[recipiant] - value) < 0) {
                        tokens[recipiant] = 0;
                } else {
                        tokens[recipiant] -= value;
                }
                emit OnValueChanged(recipiant, tokens[recipiant]);
                return true;
        }
        function getTokens(address recipiant) public returns (uint value) {
                return tokens[recipiant];
        }
}
