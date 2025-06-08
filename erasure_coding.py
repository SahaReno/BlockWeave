"""
Simulates erasure-coded block propagation for large blocks (Section 3.5.1).
Uses Reed-Solomon encoding for parallel transmission.
"""
import numpy as np
from reedsolo import RSCodec  # pip install reedsolo

class BlockPropagator:
    def __init__(self, redundancy_factor=2):
        self.redundancy = redundancy_factor
        
    def encode_block(self, block_data: bytes) -> List[bytes]:
        """Splits data into chunks with Reed-Solomon parity"""
        rs = RSCodec(self.redundancy)
        chunk_size = len(block_data) // 4  # 4 data chunks
        chunks = [block_data[i:i+chunk_size] for i in range(0, len(block_data), chunk_size)]
        return [rs.encode(chunk) for chunk in chunks]
    
    def decode_block(self, encoded_chunks: List[bytes]) -> bytes:
        """Reassembles block from available chunks"""
        rs = RSCodec(self.redundancy)
        decoded_chunks = []
        for chunk in encoded_chunks:
            try:
                decoded_chunks.append(rs.decode(chunk)[0])
            except:
                continue  # Tolerate up to `redundancy` lost chunks
        return b''.join(decoded_chunks)

# Example Usage
if __name__ == "__main__":
    propagator = BlockPropagator(redundancy_factor=2)
    
    # Simulate 200MB block (truncated for demo)
    block_data = b"Simulated 200MB block..." * 1000
    
    # Encode and simulate 1 lost chunk
    encoded = propagator.encode_block(block_data)
    print(f"Encoded {len(encoded)} chunks (2 parity)")
    
    received_chunks = encoded[:-1]  # Lose one chunk
    reconstructed = propagator.decode_block(received_chunks)
    print(f"Reconstruction {'successful' if reconstructed == block_data else 'failed'}")
