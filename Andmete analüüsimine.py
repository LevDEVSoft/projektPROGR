def analyze_trends(data):

#    Analüüsime andmete trende (nt temperatuuri ja valguse taseme muutusi).
#    Kas trend on stabiilne või kasvav. Määrame selleks lihtsustava analüüsi

    trend = "Stabiilne" if data[-1] == data[0] else "Kasvav"
    return trend
