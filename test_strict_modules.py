"""
Rigorous test for strict module-specific question generation
"""
import asyncio
from app.agents.question_generator import question_generator
from app.models import QuestionGenerationRequest, TestType

async def test_strict_module_filtering():
    """Test that questions are generated ONLY from selected modules"""
    
    # Create a very detailed syllabus with clear module separation
    detailed_syllabus = """
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

Module 4: Network Layer and IP
- IPv4 addressing and subnetting
- IPv6 introduction and benefits
- Routing algorithms: Distance vector, Link state
- Routing protocols: RIP, OSPF, BGP
- Network Address Translation (NAT)

Module 5: Transport Layer Services
- TCP vs UDP comparison
- Connection establishment: 3-way handshake
- Flow control and congestion control
- Port numbers and socket programming
- Reliable data transfer mechanisms

Module 6: Application Layer Protocols
- Domain Name System (DNS)
- Web protocols: HTTP, HTTPS
- Email protocols: SMTP, POP3, IMAP  
- File Transfer Protocol (FTP)
- Network management: SNMP

Module 7: Network Security Fundamentals
- Cryptographic techniques
- Authentication and authorization
- Firewalls and intrusion detection
- VPN and secure tunneling
- Wireless security protocols

Module 8: Network Performance Analysis
- Traffic analysis and monitoring
- Quality of Service (QoS)
- Network optimization techniques
- Bandwidth utilization measurement
- Performance bottleneck identification

Module 9: Wireless and Mobile Networks
- Wireless communication principles
- IEEE 802.11 standards (WiFi)
- Mobile IP and cellular networks
- Bluetooth and personal area networks
- Wireless security challenges

Module 10: Emerging Network Technologies
- Software Defined Networking (SDN)
- Network Function Virtualization (NFV)
- Cloud networking concepts
- Internet of Things (IoT) networking
- 5G and beyond wireless technologies
"""

    print("=== TESTING STRICT MODULE FILTERING ===\n")
    
    # Test Case 1: Only Module 2 and Module 5 - very specific selection
    print("🔍 Test 1: Requesting ONLY Module 2 and Module 5")
    print("Expected: Questions about Physical Layer and Transport Layer ONLY")
    print("Forbidden: Any questions about other topics (network fundamentals, IP, DNS, security, etc.)")
    
    request1 = QuestionGenerationRequest(
        syllabus_text=detailed_syllabus,
        test_type=TestType.CAT1,
        modules=["Module 2", "Module 5"]
    )
    
    try:
        result1 = await question_generator.generate_question_paper(request1)
        
        if result1.success:
            print("✅ Generation successful!")
            
            # Analyze each question in detail
            forbidden_topics = [
                "network types", "topology", "osi model", "router", "switch", "hub", "gateway",  # Module 1
                "frame", "mac address", "ethernet", "vlan", "arp",  # Module 3  
                "ip address", "subnet", "routing", "ospf", "rip", "bgp", "nat",  # Module 4
                "dns", "http", "smtp", "ftp", "email", "web",  # Module 6
                "security", "firewall", "vpn", "encryption", "authentication",  # Module 7
                "performance", "qos", "monitoring", "optimization",  # Module 8
                "wireless", "wifi", "bluetooth", "mobile", "cellular",  # Module 9
                "sdn", "nfv", "cloud", "iot", "5g"  # Module 10
            ]
            
            allowed_topics = [
                "transmission media", "fiber", "copper", "wireless transmission", "signal encoding", "bandwidth", "error detection", "parity", "crc",  # Module 2
                "tcp", "udp", "connection", "handshake", "flow control", "congestion", "port", "socket", "reliable"  # Module 5
            ]
            
            violations = []
            correct_questions = []
            
            for i, question in enumerate(result1.question_paper.paper, 1):
                question_text = question.parts[0].text.lower()
                question_modules = question.parts[0].module
                
                print(f"\nQ{i}: {question.parts[0].text}")
                print(f"Tagged modules: {question_modules}")
                
                # Check for forbidden content
                found_forbidden = [topic for topic in forbidden_topics if topic in question_text]
                found_allowed = [topic for topic in allowed_topics if topic in question_text]
                
                if found_forbidden:
                    violations.append(f"Q{i} contains forbidden topics: {found_forbidden}")
                    print(f"❌ VIOLATION: Contains forbidden topics: {found_forbidden}")
                
                # Check module tagging
                invalid_modules = [mod for mod in question_modules if mod not in ["Module 2", "Module 5"]]
                if invalid_modules:
                    violations.append(f"Q{i} tagged with wrong modules: {invalid_modules}")
                    print(f"❌ VIOLATION: Wrong module tags: {invalid_modules}")
                
                if not found_forbidden and not invalid_modules:
                    correct_questions.append(i)
                    print(f"✅ CORRECT: Module-specific content")
            
            print(f"\n📊 RESULTS:")
            print(f"Total questions: {len(result1.question_paper.paper)}")
            print(f"Correct questions: {len(correct_questions)}")
            print(f"Violations: {len(violations)}")
            
            if violations:
                print(f"\n❌ VIOLATIONS FOUND:")
                for violation in violations:
                    print(f"  - {violation}")
            else:
                print(f"\n🎉 PERFECT! All questions are module-specific!")
                
        else:
            print(f"❌ Generation failed: {result1.message}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)

if __name__ == "__main__":
    asyncio.run(test_strict_module_filtering())