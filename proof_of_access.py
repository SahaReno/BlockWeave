"""
Simulates Proof-of-Access (PoA) consensus for Blockweave.
Validates blocks by requiring miners to prove access to historical data.
"""
import hashlib
import random
from typing import List, Dict

class Block:
    def __init__(self, height: int, prev_hash: str, transactions: List[str], old_block_ref: str):
        self.height = height
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.old_block_ref = old_block_ref  # Reference to a historical block
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_data = f"{self.height}{self.prev_hash}{self.old_block_ref}{''.join(self.transactions)}"
        return hashlib.sha384(block_data.encode()).hexdigest()

class PoANetwork:
    def __init__(self):
        self.blocks: List[Block] = []
        self.historical_blocks: Dict[str, Block] = {}  # Simulates Arweave's blockweave

    def validate_block(self, block: Block) -> bool:
        """Check if miner can access the referenced historical block"""
        return block.old_block_ref in self.historical_blocks

    def add_block(self, block: Block):
        if self.validate_block(block):
            self.blocks.append(block)
            self.historical_blocks[block.hash] = block
            print(f"Block {block.height} mined ✓ (Ref: {block.old_block_ref[:8]}...)")
        else:
            print(f"Block {block.height} rejected: Missing historical data")

# Example Usage
if __name__ == "__main__":
    network = PoANetwork()
    
    # Genesis block
    genesis = Block(0, "0", ["TX0"], "0")
    network.historical_blocks[genesis.hash] = genesis
    
    # Simulate mining
    for i in range(1, 5):
        old_ref = random.choice(list(network.historical_blocks.keys()))
        new_block = Block(i, network.blocks[-1].hash, [f"TX{i}"], old_ref)
        network.add_block(new_block)
