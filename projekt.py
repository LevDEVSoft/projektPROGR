################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Tark Energiasäästja
#
# Autorid:
#   Leonard Lume
#   Lev Listov
#
# Lisakommentaar:
#   Käivitusjuhend:
#   1) Käivita programm (Python 3.x)
#   2) Programmi avaneb graafiline aken (tkinter)
#   3) Kasutaja saab sisestada temperatuuriväärtusi. Iga sisestuse järel 
#      lisatakse ka juhuslik valguse väärtus, mis simuleerib valgusandurilt kogutud andmeid.
#   4) Kui kasutaja on andmed sisestanud, vajutab ta "Lisa andmed".
#   5) Andmed lisatakse listidesse ja kuvatakse trend (kasvav, langev, stabiilne) 
#      ning soovitused energiakasutuse optimeerimiseks.
#   6) Kasutaja saab andmeid uuendada mitu korda, sisestades järjest uusi temperatuuriväärtusi.
#
#   
#   
##################################################

import tkinter as tk
import random


def analyze_trends(data):
    """
    Analüüsib andmete trende.
    
    Parameetrid:
        data (list): numbriline andmelist, mille põhjal trendi määratakse.
        
    Tagastab:
        str: "Kasvav"  - kui viimane väärtus on suurem kui esimene
             "Langev"  - kui viimane väärtus on väiksem kui esimene
             "Stabiilne" - kui viimane ja esimene väärtus on võrdsed
             "Pole piisavalt andmeid" - kui andmed puuduvad või liiga vähe
    """
    if not data or len(data) < 2:
        # Kui andmeid pole või on vaid üks punkt, pole trendianalüüs võimalik
        return "Pole piisavalt andmeid"
    if data[-1] > data[0]:
        return "Kasvav"
    elif data[-1] < data[0]:
        return "Langev"
    else:
        return "Stabiilne"


def generate_light_data():
    """
    Genereerib juhusliku valguse intensiivsuse väärtuse.
    
    Tagastab:
        float: juhuslik valguse intensiivsus luksides vahemikus 100-500.
        
    Tegelikkuses tuleks siia panna andurilt lugemise loogika või
    reaalsete andmete kasutus andmebaasist, failist või API-st.
    """
    return random.uniform(100, 500)


def provide_suggestions(temp_data, light_data):
    """
    Tagastab soovitused energiakasutuse optimeerimiseks, lähtuvalt olemasolevast
    temperatuurist ja valgusest.
    
    Loogika:
    - Arvutame temperatuuride keskmise.
      Kui keskmine temperatuur > 22°C: soovitame kütet vähendada.
      Muidu: ütleme, et temperatuur on hea.
      
    - Arvutame valguse keskmise.
      Kui keskmine valgus > 300 luks: soovitame valgustuse vähendamist.
      Muidu: ütleme, et valgus on sobilik.
      
    Parameetrid:
        temp_data (list): temperatuuride andmelist
        light_data (list): valguse andmelist
        
    Tagastab:
        str: soovitused sõnalises vormis
    """
    if not temp_data or not light_data:
        # Kui andmeid pole, ei saa anda soovitusi
        return "Pole piisavalt andmeid soovituste andmiseks."
    
    # Arvutame keskmise temperatuuri
    avg_temp = sum(temp_data)/len(temp_data)
    # Arvutame keskmise valguse
    avg_light = sum(light_data)/len(light_data)
    
    suggestions = []
    
    # Temperatuuri soovitused
    if avg_temp > 22:
        suggestions.append("Temperatuur on kõrge, kaalu kütte vähendamist.")
    else:
        suggestions.append("Temperatuur on heas vahemikus.")
        
    # Valguse soovitused
    if avg_light > 300:
        suggestions.append("Valgustase on kõrge, kaalu valgustuse vähendamist.")
    else:
        suggestions.append("Valgustase on sobilik.")
    
    # Liidame soovitused ühte lausesse
    return " ".join(suggestions)


def add_data():
    """
    Lisa kasutaja sisestatud temperatuur ja genereeri uus valguse väärtus andmelistidesse.
    Seejärel uuendatakse trende, kuvamist listboxides ja soovitusi graafilises liideses.
    """
    temp_input = entry_temp.get()
    if not temp_input:
        # Kui kasutaja ei sisestanud midagi
        label_status.config(text="Sisesta temperatuur!")
        return
    
    try:
        # Kontrollime, kas sisestus on arv
        temp_value = float(temp_input)
    except ValueError:
        # Väär sisend (ei ole numbrit)
        label_status.config(text="Vigane temperatuuri väärtus!")
        return
    
    # Lisa temperatuur andmelisti
    temperature_data.append(temp_value)
    
    # Lisa valgus juhusliku väärtuse alusel
    val = generate_light_data()
    light_data.append(val)
    
    # Uuendame trendid temperatuuride ja valguse kohta
    temp_trend = analyze_trends(temperature_data)
    light_trend = analyze_trends(light_data)
    
    # Kuvame trendid liideses
    label_temp_trend.config(text=f"Temperatuuri trend: {temp_trend}")
    label_light_trend.config(text=f"Valguse trend: {light_trend}")
    
    # Uuendame Listboxe temperatuuride ja valgusandmetega
    listbox_temp.delete(0, tk.END)
    for t in temperature_data:
        listbox_temp.insert(tk.END, f"{t:.2f} °C")
        
    listbox_light.delete(0, tk.END)
    for l in light_data:
        listbox_light.insert(tk.END, f"{l:.2f} luks")
    
    # Loome soovitused ja kuvame need liideses
    sugg = provide_suggestions(temperature_data, light_data)
    label_suggestions.config(text=f"Soovitused: {sugg}")
    
    # Tühjendame sisestusvälja, et oleks mugavam uusi andmeid lisada
    entry_temp.delete(0, tk.END)
    
    # Kuvame staatusteate, et andmed lisati edukalt
    label_status.config(text="Andmed lisatud.")


def main():
    """
    Põhiprogramm, mis loob graafilise kasutajaliidese, kus kasutaja saab sisestada 
    temperatuuriväärtusi. Iga sisestuse järel lisatakse ka valguse andmepunkt (juhuslik),
    analüüsitakse trende ja antakse soovitusi.
    
    Selle programmi eesmärk on aidata kasutajal jälgida energiakasutuse trende.
    Näiteks on kõrge temperatuuri korral võimalik soojuskulusid vähendada ning
    liiga kõrge valguse korral optimeerida valgustuse energiat.
    """
    global temperature_data, light_data
    global entry_temp, label_status, label_temp_trend, label_light_trend, label_suggestions
    global listbox_temp, listbox_light

    # Algandmed tühjad
    temperature_data = []
    light_data = []

    # Loome graafilise liidese juurakna
    root = tk.Tk()
    root.title("Tark Energiasäästja")

    # Sisestusväli ja nupp "Lisa andmed"
    frame_input = tk.Frame(root)
    frame_input.pack(pady=10)

    tk.Label(frame_input, text="Sisesta temperatuur (°C):").pack(side=tk.LEFT, padx=5)
    entry_temp = tk.Entry(frame_input)
    entry_temp.pack(side=tk.LEFT, padx=5)
    btn_add = tk.Button(frame_input, text="Lisa andmed", command=add_data)
    btn_add.pack(side=tk.LEFT, padx=5)

    # Staatusteade kasutajale
    label_status = tk.Label(root, text="")
    label_status.pack(pady=5)

    # Trendide kuvamise sektsioon
    frame_trends = tk.Frame(root)
    frame_trends.pack(pady=10)

    label_temp_trend = tk.Label(frame_trends, text="Temperatuuri trend: Puudub")
    label_temp_trend.pack(side=tk.LEFT, padx=10)

    label_light_trend = tk.Label(frame_trends, text="Valguse trend: Puudub")
    label_light_trend.pack(side=tk.LEFT, padx=10)

    # Andmete kuvamine listides
    frame_data = tk.Frame(root)
    frame_data.pack(pady=10)

    # Temperatuuride listbox ja pealkiri
    frame_temp = tk.Frame(frame_data)
    frame_temp.pack(side=tk.LEFT, padx=10)
    tk.Label(frame_temp, text="Temperatuuri andmed:").pack()
    listbox_temp = tk.Listbox(frame_temp, width=20, height=8)
    listbox_temp.pack(pady=5)

    # Valguse listbox ja pealkiri
    frame_light = tk.Frame(frame_data)
    frame_light.pack(side=tk.LEFT, padx=10)
    tk.Label(frame_light, text="Valguse andmed:").pack()
    listbox_light = tk.Listbox(frame_light, width=20, height=8)
    listbox_light.pack(pady=5)

    # Soovituste silt
    label_suggestions = tk.Label(root, text="Soovitused: ")
    label_suggestions.pack(pady=10)

    # Käivitame GUI tsükli
    root.mainloop()


if __name__ == "__main__":
    main()
