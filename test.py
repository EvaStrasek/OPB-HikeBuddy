from Services.poti_nova_service import GoraPotService

def main():
    service = GoraPotService()
    
    print("Prvih 10 poti:")
    poti = service.dobi_poti()
    
    for i, pot in enumerate(poti[:10], start=1):
        print(f"{i}. {pot}")

if __name__ == "__main__":
    main()
