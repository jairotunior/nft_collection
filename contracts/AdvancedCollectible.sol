pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721URIStorage , VRFConsumerBase {

    bytes32 internal keyHash;
    uint256 internal fee;

    uint256 public tokenCounter;

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => uint256) public requestIdToTokenId;

    event requestedCollectible(bytes32 indexed requestId);

    enum Breed{ PUG, SHIBA_INU, ST_BERNARD }

    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash)
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Doggies", "DOG")
    {
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18; // 0.1 LINK (Varies by network)
        tokenCounter = 0;
    }

    function createCollectible(uint256 userProvidedSeed, string memory tokenURI)
    public returns (bytes32)
    {
        //bytes32 requestId = requestRandomness(keyHash, fee, userProvidedSeed);
        bytes32 requestId = requestRandomness(keyHash, fee);

        // Request associeated with me
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        
        // Next line is for testing
        emit requestedCollectible(requestId);
    }

    /**
     * Callback function used by VRF Coordinator
    */
    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        address dogOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        
        _safeMint(dogOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);

        Breed breed = Breed(randomness % 3);
        tokenIdToBreed[newItemId] = breed;
        requestIdToTokenId[requestId] = newItemId;

        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, tokenURI);
    }
}