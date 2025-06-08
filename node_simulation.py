"""
Simulates Tier-S decentralized node behavior (Section 4.1).
Models geographic distribution and hardware constraints.
"""
import random
from dataclasses import dataclass
from typing import List

@dataclass
class NodeConfig:
    cpu: str  # e.g., "i5-10400F"
    ram_gb: int
    country: str
    bandwidth_mbps: int

class DecentralizedNetwork:
    def __init__(self, node_count=500):
        self.nodes = self._generate_nodes(node_count)
        
    def _generate_nodes(self, count) -> List[NodeConfig]:
        countries = ["USA", "China", "India", "Germany", "Japan", "Brazil"]
        return [
            NodeConfig(
                cpu="i5-10400F" if random.random() > 0.3 else "i3-10100",
                ram_gb=8 if random.random() > 0.2 else 16,
                country=random.choice(countries),
                bandwidth_mbps=random.randint(10, 100)
            )
            for _ in range(count)
        ]
    
    def analyze_decentralization(self):
        """Calculates Tier-S metrics (Section 4.1.3)"""
        country_dist = {}
        for node in self.nodes:
            country_dist[node.country] = country_dist.get(node.country, 0) + 1
        
        max_share = max(country_dist.values()) / len(self.nodes)
        print(f"Nodes: {len(self.nodes)} | Countries: {len(country_dist)}")
        print(f"Max country share: {max_share:.1%} (<15% for Tier-S)")
        print(f"Hardware uniformity: {sum(1 for n in self.nodes if n.cpu == 'i5-10400F') / len(self.nodes):.1%}")

# Example Usage
if __name__ == "__main__":
    network = DecentralizedNetwork(node_count=500)
    network.analyze_decentralization()
