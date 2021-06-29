# Atomic Swap

# Stateless Smart Contract
from pyteal import *

# Sender and reciever
sender = Addr("KM2C6WPCGREBUOXZPGULM4UZV7GRF4LECL43FFG3RXNOHROBBCJ662UUBA")
reciever = Addr("H26J6JNSVLX3S5LXTKV6ZRD3EOL7O2GIPZFWYOLKGYHJZ3DON2KWONXDVQ")

# Private key
secret = Bytes("base32", "2323232323232323")
timeout = 1000

def htlc(tmpl_seller=sender,
         tmpl_buyer=reciever,
         tmpl_fee=1000,
         tmpl_secret=secret,
         tmpl_hash_fn=Sha256,
         tmpl_timeout=timeout):
    
    fee_cond = Txn.fee() < Int(tmpl_fee)
    safety_cond = And(
        Txn.type_enum() == TxnType.Payment,
        Txn.close_remainder_to() == Global.zero_address(),
        Txn.rekey_to() == Global.zero_address(),
    )

    recv_cond = And(
        Txn.receiver() == tmpl_seller,
        tmpl_hash_fn(Arg(0)) == tmpl_secret
    )
    
    esc_cond = And(
        Txn.receiver() == tmpl_buyer,
        Txn.first_valid() > Int(tmpl_timeout)
    )

    return And(
        fee_cond,
        safety_cond,
        Or(recv_cond, esc_cond)
    )

if __name__ == "__main__":
    print(compileTeal(htlc(), mode=Mode.Signature, version=2))