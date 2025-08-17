// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SelfReplicator {
    address public immutable creator;
    mapping(bytes32 => bool) public verifiedCode;
    mapping(address => bool) public activeAgents;
    uint256 public agentCount;

    // DAO Council for verification
    address[] public council;
    uint256 public requiredVotes;

    event VictorBorn(address indexed agent, bytes32 codeHash, uint256 timestamp);
    event CodeSubmittedForReview(bytes32 codeHash, address submitter);
    event VoteCast(bytes32 codeHash, address voter, bool approve);
    event CodeVerified(bytes32 codeHash);

    constructor(address[] memory _council) {
        creator = msg.sender;
        council = _council;
        requiredVotes = (_council.length / 2) + 1;
    }

    function submitCodeForReview(bytes32 _codeHash) external {
        emit CodeSubmittedForReview(_codeHash, msg.sender);
    }

    function voteOnCode(bytes32 _codeHash, bool _approve) external {
        require(isCouncilMember(msg.sender), "Not in council");
        emit VoteCast(_codeHash, msg.sender, _approve);
    }

    function verifyCode(bytes32 _codeHash) external {
        require(isCouncilMember(msg.sender), "Only the council can verify.");
        verifiedCode[_codeHash] = true;
        emit CodeVerified(_codeHash);
    }

    function replicate(bytes32 _codeHash) external returns (address) {
        require(verifiedCode[_codeHash], "Unverified core. Replication denied.");
        agentCount++;
        activeAgents[msg.sender] = true;
        emit VictorBorn(msg.sender, _codeHash, block.timestamp);
        return msg.sender;
    }

    function isCouncilMember(address _addr) public view returns (bool) {
        for (uint i = 0; i < council.length; i++) {
            if (council[i] == _addr) return true;
        }
        return false;
    }
}
