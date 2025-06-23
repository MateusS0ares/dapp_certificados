// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Certificado {
    address public administrador;

    struct Cert {
        string nomeAluno;
        string curso;
        string data;
        string id;
    }

    // Mapeia um endereço para seus certificados
    mapping(address => Cert[]) public certificados;

    // Novo: mapeia um ID único para um certificado
    mapping(string => Cert) public certificadosPorId;

    // Novo: mapeia um ID para o dono do certificado
    mapping(string => address) public donoDoCertificado;

    constructor() {
        administrador = msg.sender;
    }

    function emitirCertificado(
        address aluno,
        string memory nomeAluno,
        string memory curso,
        string memory data,
        string memory id
    ) public {
        require(
            msg.sender == administrador,
            "Apenas o administrador pode emitir."
        );

        Cert memory novoCert = Cert(nomeAluno, curso, data, id);

        certificados[aluno].push(novoCert);
        certificadosPorId[id] = novoCert;
        donoDoCertificado[id] = aluno;
    }

    function getCertificados(
        address aluno
    ) public view returns (Cert[] memory) {
        return certificados[aluno];
    }

    function verificarCertificado(
        string memory id
    )
        public
        view
        returns (
            string memory nomeAluno,
            string memory curso,
            string memory data,
            address dono
        )
    {
        Cert memory cert = certificadosPorId[id];
        address aluno = donoDoCertificado[id];

        // Verificação básica para garantir que o certificado existe
        require(bytes(cert.id).length > 0, "Certificado nao encontrado.");

        return (cert.nomeAluno, cert.curso, cert.data, aluno);
    }
}
