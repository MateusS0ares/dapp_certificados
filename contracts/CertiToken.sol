// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CertiToken is ERC20, Ownable {
    constructor() ERC20("CertiToken", "CTK") {}

    function recompensa(address aluno, uint256 quantidade) public onlyOwner {
        _mint(aluno, quantidade);
    }

    function queimar(address aluno, uint256 quantidade) public onlyOwner {
        _burn(aluno, quantidade);
    }
}
