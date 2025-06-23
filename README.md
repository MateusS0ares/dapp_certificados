# Trabalho Dapp - Emissão de Certificados usando Blockchain

Este projeto é um sistema descentralizado para emissão de certificados utilizando tecnologia blockchain. O objetivo é garantir a autenticidade e a imutabilidade dos certificados emitidos, proporcionando uma solução segura e transparente para instituições de ensino e alunos.

## Como Funciona
1. **Emissão de Certificados**: É possível emitir certificados digitais que são registrados na blockchain, garantindo que não possam ser alterados ou falsificados.

2. **Verificação de Certificados**: Qualquer pessoa pode verificar a autenticidade de um certificado consultando a blockchain, garantindo que o documento é legítimo e foi emitido corretamente.

3. **Armazenamento Descentralizado**: Os certificados são armazenados de forma descentralizada, evitando o risco de perda ou manipulação de dados.

## Tecnologias Utilizadas
- **Solidity**: Linguagem de programação para contratos inteligentes na blockchain Ethereum.

- **Biblioteca Web3 Python**: Utilizada para interagir com a blockchain Ethereum.

- **Biblioteca Account Python**: Para manipulação de contas e transações na blockchain.

- **MetaMask**: Extensão de navegador que permite interagir com a blockchain Ethereum de forma segura.

- **Remix IDE**: Ambiente de desenvolvimento para escrever, testar e implantar contratos inteligentes em Solidity.

- **Alchemy**: Plataforma que fornece uma API para interagir com a blockchain Ethereum, facilitando o desenvolvimento de dApps.

- **Google Cloud Web3 Ethereum Sepolia Faucet**: Utilizada para obter Ether de teste na rede Sepolia, permitindo a realização de transações sem custo real.

## Instalação e Configuração
Siga os passos abaixo para configurar e executar o projeto:

### 1. Clone o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd dapp_certificados
```
### 2. Crie e ative um ambiente virtual
No Linux/MacOS:
```bash
python3 -m venv dapp_certificados
source dapp_certificados/bin/activate
```
No Windows:
```bash
python -m venv dapp_certificados
dapp_certificados\Scripts\activate
```
### 3. Instale as dependências
```bash
pip install web3 flask python-dotenv
```

### 4. Configure as variáveis de ambiente
Copie o arquivo `.env.example` para `.env` e preencha as variáveis com suas informações:
```bash
cp .env.example .env
```
### 5. Execute o cliente Flask
```bash
python app.py
```
### 6. Acesse a aplicação
Abra o navegador e acesse `http://localhost:5000` para ver a interface do cliente Flask.

## Interface da aplicação
![Index](https://github.com/MateusS0ares/dapp_certificados/blob/main/static/img/index.png?raw=true)

![Admin](https://github.com/MateusS0ares/dapp_certificados/blob/main/static/img/admin.png?raw=true)

![Aluno](https://github.com/MateusS0ares/dapp_certificados/blob/main/static/img/student.png?raw=true)
