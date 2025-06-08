"""
Implements Blockweave's UTXO anchoring mechanism to prevent double-spending.
Section 3.4 of the paper.
"""
import hashlib
from dataclasses import dataclass
from typing import List, Dict
from merkletools import MerkleTools  # pip install merkletools

@dataclass
class UTXO:
    tx_id: str
    output_index: int
    amount: float
    address: str

class UTXOAnchorChain:
    def __init__(self):
        self.utxo_pool: Dict[str, UTXO] = {}  # Unspent UTXOs
        self.merkle_tool = MerkleTools(hash_type='sha384')
        
    def add_utxos(self, utxos: List[UTXO]):
        """Add new UTXOs to the pool and update Merkle root"""
        for utxo in utxos:
            self.utxo_pool[f"{utxo.tx_id}:{utxo.output_index}"] = utxo
        
        # Rebuild Merkle tree
        self.merkle_tool.reset_tree()
        for utxo_key in sorted(self.utxo_pool.keys()):
            self.merkle_tool.add_leaf(utxo_key.encode())
        self.merkle_tool.make_tree()
        
    def verify_input(self, tx_id: str, output_index: int) -> bool:
        """Check if UTXO exists and is unspent (Eq. 10)"""
        return f"{tx_id}:{output_index}" in self.utxo_pool

    def get_merkle_root(self) -> str:
        """Returns current root hash of the UTXO set"""
        return self.merkle_tool.get_merkle_root()

# Example Usage
if __name__ == "__main__":
    anchor_chain = UTXOAnchorChain()
    
    # Sample UTXOs
    utxos = [
        UTXO("TX0001", 0, 150.0, "0xA3f1...b9DE"),
        UTXO("TX0002", 1, 75.0, "0xC4e2...77F1")
    ]
    
    anchor_chain.add_utxos(utxos)
    print(f"Merkle Root: {anchor_chain.get_merkle_root()}")
    print(f"Verify TX0001:0: {anchor_chain.verify_input('TX0001', 0)}")  # True
    print(f"Verify TX0003:0: {anchor_chain.verify_input('TX0003', 0)}")  # False
