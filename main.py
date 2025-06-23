from web3 import Web3
from eth_account import Account
import json
import os
from dotenv import load_dotenv

load_dotenv()

# === 1. Conectar à Sepolia via Alchemy ===
alchemy_url = os.getenv("ALCHEMY_URL")  # coloque no .env
w3 = Web3(Web3.HTTPProvider(alchemy_url))

if not w3.is_connected():
    raise Exception("❌ Não foi possível conectar ao Alchemy/Sepolia.")

# === 2. Carregar contrato Certificado ===
with open("contracts/CertificadoABI.json") as f:
    certificado_abi = json.load(f)

endereco_contrato = os.getenv("CERTIFICADO_ADDRESS")
endereco_contrato_checksum = Web3.to_checksum_address(endereco_contrato)


contrato_certificado = w3.eth.contract(
    address=endereco_contrato_checksum,
    abi=certificado_abi
)

# === 2.1 Carregar contrato Certitoken ===
with open("contracts/CertiTokenABI.json") as f:
    certitoken_abi = json.load(f)
    
endereco_certitoken = os.getenv("CERTITOKEN_ADDRESS")
endereco_certitoken_checksum = Web3.to_checksum_address(endereco_certitoken)


certitoken = w3.eth.contract(
    address=endereco_certitoken_checksum,
    abi=certitoken_abi
)

# === 3. Chave do admin (MetaMask) ===
chave_privada = os.getenv("CHAVE_PRIVADA")
admin = Account.from_key(chave_privada)
endereco_admin = admin.address

# === 4. Emitir certificado ===
def emitir_certificado(aluno, nome, curso, data, id_cert):
    try:
        print(f"[DEBUG] Iniciando emissão do certificado para: {aluno}")
        nonce = w3.eth.get_transaction_count(endereco_admin)
        print(f"[DEBUG] Nonce atual: {nonce}")

        tx = contrato_certificado.functions.emitirCertificado(
            aluno, nome, curso, data, id_cert
        ).build_transaction({
            'from': endereco_admin,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': w3.to_wei('10', 'gwei')
        })
        print("[DEBUG] Transação construída com sucesso")

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=chave_privada)
        print("[DEBUG] Transação assinada")

        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"[DEBUG] Transação enviada, hash: {tx_hash.hex()}")

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"[DEBUG] Receipt recebido: {receipt}")

        if receipt.status == 1:
            print("[DEBUG] Transação confirmada com sucesso")
        else:
            print("[DEBUG] Transação falhou")

        return tx_hash.hex()
    except Exception as e:
        print(f"[ERROR] Erro ao emitir certificado: {e}")
        raise Exception(f"Erro ao emitir certificado: {e}")

# === 5. Ver certificados ===
def ver_certificados(aluno):
    try:
        print(f"[DEBUG] Consultando certificados para: {aluno}")
        certificados = contrato_certificado.functions.getCertificados(aluno).call()
        print(f"[DEBUG] Certificados recebidos: {certificados}")
        return certificados
    except Exception as e:
        print(f"[ERROR] Erro ao buscar certificados: {e}")
        raise Exception(f"Erro ao buscar certificados: {e}")
    
# === 6. Ver Saldo ===
def ver_saldo(endereco):
    return certitoken.functions.balanceOf(Web3.to_checksum_address(endereco)).call()

# === 7. Transferir Token ===
def transferir_token(remetente_priv_key, destinatario, quantidade):
    try:
        conta = Account.from_key(remetente_priv_key)
        print(f"Endereço remetente: {conta.address}")
        nonce = w3.eth.get_transaction_count(conta.address)
        print(f"Nonce atual: {nonce}")

        tx = certitoken.functions.transfer(destinatario, quantidade).build_transaction({
            'from': conta.address,
            'nonce': nonce,
            'gas': 100000,
            'gasPrice': w3.to_wei('10', 'gwei')
        })

        print("Transação construída:", tx)

        signed = w3.eth.account.sign_transaction(tx, private_key=remetente_priv_key)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

        print(f"Transação enviada, hash: {tx_hash.hex()}")
        return tx_hash.hex()

    except Exception as e:
        print(f"Erro na transferência: {e}")
        raise


# === 8. Queimar Token ===
def queimar_token(admin_priv_key, aluno, quantidade):
    conta = Account.from_key(admin_priv_key)
    nonce = w3.eth.get_transaction_count(conta.address)
    tx = certitoken.functions.queimar(aluno, quantidade).build_transaction({
        'from': conta.address,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': w3.to_wei('10', 'gwei')
    })
    signed = w3.eth.account.sign_transaction(tx, private_key=admin_priv_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return tx_hash.hex()