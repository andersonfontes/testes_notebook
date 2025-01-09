import wmi

def get_battery_health():
    try:
        c = wmi.WMI(namespace="root\\WMI")
        
        # Tenta obter as capacidades usando BatteryFullChargedCapacity e BatteryStaticData
        full_charge = c.query("SELECT * FROM BatteryFullChargedCapacity")
        design_capacity = c.query("SELECT * FROM BatteryStaticData")

        if full_charge and design_capacity:
            # Tenta acessar as propriedades se estiverem disponíveis
            full_charge_capacity = full_charge[0].FullChargedCapacity
            original_capacity = design_capacity[0].DesignedCapacity

            if full_charge_capacity and original_capacity:
                health_percentage = (full_charge_capacity / original_capacity) * 100
                return f"{health_percentage:.2f}%"
        return "Desconhecido"
    except Exception as e:
        print(f"Erro ao obter a saúde da bateria: {e}")
        return "Desconhecido"

# Teste (opcional)
if __name__ == "__main__":
    print("Saúde da Bateria:", get_battery_health())
