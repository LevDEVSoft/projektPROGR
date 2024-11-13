def collect_data(sensor_type):
    
#    Andmete kogumine erinvatest anduritest (nt temperatuur, valgus).
 #   Tagastab testväärtuse, mida hiljem saab asendada tegeliku anduriga.
    
    if sensor_type == "temperature":
        return 22.5  # Näiteks temperatuur, väärtus Celsiuse järgi
    elif sensor_type == "light":
        return 500  # Näiteks valgus, väärtus luksides
    return 0
#Siin me määrasime kõik funktsioonid, andmete kogumise funktsioonid
# Veel kasutasime need funktsioonid, mis analüüsivad andmed