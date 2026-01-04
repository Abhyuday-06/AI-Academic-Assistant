"""
Debug the module extraction to see what content is being extracted
"""
from app.agents.question_generator import question_generator

def debug_extraction():
    # Test syllabus
    syllabus = """
Computer Networks - Complete Syllabus

Module 1: Network Fundamentals
- Introduction to computer networks
- Network types: LAN, WAN, MAN
- Network topologies: Star, Ring, Mesh, Bus
- OSI Reference Model - 7 layers
- Network devices: Hub, Switch, Router, Gateway

Module 2: Physical Layer Communication  
- Transmission media: Copper wire, Fiber optics, Wireless
- Signal encoding techniques
- Digital vs Analog transmission
- Bandwidth and data rate concepts
- Error detection methods: Parity, CRC

Module 3: Data Link Layer Protocols
- Frame formatting and synchronization
- MAC addressing and ARP protocol  
- Ethernet standards: 802.3, Fast Ethernet, Gigabit Ethernet
- Switching concepts and VLAN
- Point-to-point protocols

Module 5: Transport Layer Services
- TCP vs UDP comparison
- Connection establishment: 3-way handshake
- Flow control and congestion control
- Port numbers and socket programming
- Reliable data transfer mechanisms
"""

    print("=== DEBUGGING MODULE EXTRACTION ===\n")
    
    # Test extraction for Module 2 and 5 only
    extracted = question_generator._extract_module_content(syllabus, ["Module 2", "Module 5"])
    
    print("EXTRACTED CONTENT:")
    print("=" * 60)
    print(extracted)
    print("=" * 60)
    
    # Check if it contains any forbidden content
    forbidden_words = ["ethernet", "frame", "mac", "arp", "vlan", "switching"]
    
    print("\nCHECKING FOR FORBIDDEN CONTENT:")
    extracted_lower = extracted.lower()
    
    for word in forbidden_words:
        if word in extracted_lower:
            print(f"❌ FOUND FORBIDDEN: '{word}' in extracted content")
            # Show the context
            lines = extracted.split('\n')
            for i, line in enumerate(lines):
                if word.lower() in line.lower():
                    print(f"  Line {i+1}: {line.strip()}")
        else:
            print(f"✅ Clean: '{word}' not found")

if __name__ == "__main__":
    debug_extraction()