"""
Implements Blockweave's dynamic block sizing based on network load.
"""
class BlockSizeAdjuster:
    def __init__(self, min_size=1, max_size=200):
        self.min_size = min_size  # MB
        self.max_size = max_size
        self.current_size = min_size
        self.threshold = 0.8  # τ (default: 80% capacity)

    def update_size(self, pending_txs: int, confirmed_txs: int) -> int:
        """Adjust block size using Eq. (8) from the paper"""
        if pending_txs / confirmed_txs >= self.threshold:
            # Scale up
            self.current_size = min(
                self.current_size * (1 + (pending_txs / confirmed_txs)),
                self.max_size
            )
        else:
            # Scale down
            self.current_size = max(self.current_size * 0.9, self.min_size)
        
        return round(self.current_size, 2)

# Example Usage
if __name__ == "__main__":
    adjuster = BlockSizeAdjuster()
    
    # Simulate network load changes
    loads = [
        (1500, 1000),  # High load
        (400, 1000),   # Low load
        (900, 1000)    # Moderate load
    ]
    
    for pending, confirmed in loads:
        new_size = adjuster.update_size(pending, confirmed)
        print(f"Pending: {pending}, Confirmed: {confirmed} → Block Size: {new_size} MB")
