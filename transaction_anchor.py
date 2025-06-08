"""
Generates 48-byte Transaction Anchors (TAs) for Blockweave.
"""
import hashlib
from dataclasses import dataclass

@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    payload: bytes

def create_ta(tx: Transaction, timestamp: int) -> bytes:
    """Generates a 48-byte TA using SHA-384 (Eq. 7)"""
    data = f"{tx.sender}{tx.receiver}{tx.amount}{timestamp}".encode() + tx.payload
    return hashlib.sha384(data).digest()  # 48 bytes

# Example Usage
if __name__ == "__main__":
    tx = Transaction(
        sender="0xA3f1...b9DE",
        receiver="0xC4e2...77F1",
        amount=150.0,
        payload=b"DocumentHash123"
    )
    ta = create_ta(tx, timestamp=1625097600)
    print(f"TA (hex): {ta.hex()}\nLength: {len(ta)} bytes")
