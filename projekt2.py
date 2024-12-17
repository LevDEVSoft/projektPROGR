
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Tark Energiasäästja (lihtsustatud versioon, ilma niiskuseta)
#
# Autorid:
#   Leonard Lume
#   Lev Listov
#
# Lisakommentaar:
#   Käivitusjuhend:
#   1) Käivita programm (Python 3.x)
#   2) Avaneb graafiline aken (tkinter).
#   3) Kasutaja saab sisestada temperatuuriväärtusi (°C).
#   4) Iga andmekogumisega lisatakse ka automaatselt juhuslik valguse väärtus (luks).
#   5) Vajutades "Lisa andmed" nuppu, salvestatakse sisestatud temperatuur andmelisti,
#      genereeritakse valguse andmepunkt ning kuvatakse trendid ja soovitused.
#   6) Kasutaja saab vaadata statistikat ("Vaata statistikat" nupp), salvestada ja laadida andmeid menüü kaudu.



import tkinter as tk
import random
import csv
from tkinter import messagebox, filedialog


def analyze_trends(data):
    """
    Analüüsib andmete trende.
    
    Parameetrid:
        data (list): numbriline andmelist, mille põhjal trendi määratakse.
        
    Tagastab:
        str: "Kasvav"    - kui viimane väärtus on suurem kui esimene
             "Langev"    - kui viimane väärtus on väiksem kui esimene
             "Stabiilne" - kui viimane ja esimene väärtus on võrdsed
             "Pole piisavalt andmeid" - kui andmed puuduvad või liiga vähe
    """
    if not data or len(data) < 2:
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
    """
    return random.uniform(100, 500)


def provide_suggestions(temp_data, light_data):
    """
    Tagastab soovitused energiakasutuse optimeerimiseks, lähtuvalt temperatuurist ja valgusest.
    
    Loogika:
    - Arvutame temperatuuri keskmise:
      Kui > 22°C: soovitame kütte vähendamist.
      Muidu: temp on hea.
      
    - Arvutame valguse keskmise:
      Kui > 300 luks: soovitame valgustuse vähendamist.
      Muidu: valgus on sobilik.
    """
    if not temp_data or not light_data:
        return "Pole piisavalt andmeid soovituste andmiseks."

    avg_temp = sum(temp_data)/len(temp_data)
    avg_light = sum(light_data)/len(light_data)

    suggestions = []

    # Temperatuuri soovitused
    if avg_temp > 22:
        suggestions.append("Temperatuur kõrge, kaalu kütte vähendamist.")
    else:
        suggestions.append("Temperatuur on heas vahemikus.")

    # Valguse soovitused
    if avg_light > 300:
        suggestions.append("Valgustase kõrge, kaalu valgustuse vähendamist.")
    else:
        suggestions.append("Valgustase on sobilik.")

    return " ".join(suggestions)


def add_data():
    """
    Lisab sisestatud temperatuuri väärtuse, genereerib uue valguse väärtuse,
    uuendab trendi-, andme- ning soovituste kuvamist.
    """
    temp_input = entry_temp.get()

    if not temp_input:
        label_status.config(text="Sisesta temperatuur!")
        return
    try:
        temp_value = float(temp_input)
    except ValueError:
        label_status.config(text="Vigane temperatuur!")
        return

    # Lisame andmed listidesse
    temperature_data.append(temp_value)
    val = generate_light_data()
    light_data.append(val)

    # Uuendame trende
    temp_trend = analyze_trends(temperature_data)
    light_trend = analyze_trends(light_data)

    label_temp_trend.config(text=f"Temperatuuri trend: {temp_trend}")
    label_light_trend.config(text=f"Valguse trend: {light_trend}")

    # Uuendame listboxe
    listbox_temp.delete(0, tk.END)
    for t in temperature_data:
        listbox_temp.insert(tk.END, f"{t:.2f} °C")

    listbox_light.delete(0, tk.END)
    for l in light_data:
        listbox_light.insert(tk.END, f"{l:.2f} luks")

    # Soovitused
    sugg = provide_suggestions(temperature_data, light_data)
    label_suggestions.config(text=f"Soovitused: {sugg}")

    # Tühjendame sisestusvälja
    entry_temp.delete(0, tk.END)

    label_status.config(text="Andmed lisatud.")


def show_statistics():
    """
    Kuvab statistika (min, max, avg) eraldi teateaknas temperatuuride ja valguse kohta.
    """
    if not temperature_data or not light_data:
        messagebox.showinfo("Statistika", "Pole piisavalt andmeid statistika arvutamiseks!")
        return

    # Arvutame statistika
    def stats_str(name, data, unit):
        return (f"{name}:\n"
                f"  Min: {min(data):.2f} {unit}\n"
                f"  Max: {max(data):.2f} {unit}\n"
                f"  Keskmine: {(sum(data)/len(data)):.2f} {unit}\n")

    stat_temp = stats_str("Temperatuur", temperature_data, "°C")
    stat_light = stats_str("Valgus", light_data, "luks")

    messagebox.showinfo("Statistika", stat_temp + "\n" + stat_light)


def save_data():
    """
    Salvestab praegused andmed CSV faili.
    """
    if not temperature_data:
        messagebox.showinfo("Salvesta andmed", "Pole andmeid, mida salvestada!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", title="Vali salvestuskoht",
                                             filetypes=[("CSV failid", "*.csv"), ("All files", "*.*")])
    if not file_path:
        return  # Kasutaja katkestas

    # Salvestame CSV-sse. Iga rida: temperatuur, valgus
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Temperatuur", "Valgus"])
        for t, l in zip(temperature_data, light_data):
            writer.writerow([t, l])

    messagebox.showinfo("Salvestamine", "Andmed salvestatud!")


def load_data():
    """
    Laeb andmed CSV failist. Üle kirjutab olemasolevad andmelistid.
    """
    file_path = filedialog.askopenfilename(title="Vali andmefail",
                                           filetypes=[("CSV failid", "*.csv"), ("All files", "*.*")])
    if not file_path:
        return

    # Tühjendame olemasolevad andmed
    temperature_data.clear()
    light_data.clear()

    # Laeme failist
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = float(row["Temperatuur"])
                l = float(row["Valgus"])
                temperature_data.append(t)
                light_data.append(l)
    except Exception as e:
        messagebox.showerror("Viga", f"Andmete laadimisel ilmnes viga:\n{e}")
        return

    # Uuendame GUI
    temp_trend = analyze_trends(temperature_data)
    light_trend = analyze_trends(light_data)

    label_temp_trend.config(text=f"Temperatuuri trend: {temp_trend}")
    label_light_trend.config(text=f"Valguse trend: {light_trend}")

    listbox_temp.delete(0, tk.END)
    for t in temperature_data:
        listbox_temp.insert(tk.END, f"{t:.2f} °C")

    listbox_light.delete(0, tk.END)
    for l in light_data:
        listbox_light.insert(tk.END, f"{l:.2f} luks")

    sugg = provide_suggestions(temperature_data, light_data)
    label_suggestions.config(text=f"Soovitused: {sugg}")

    label_status.config(text="Andmed laaditud failist.")


def main():
    """
    Põhiprogramm, mis loob graafilise kasutajaliidese:
    - Saab sisestada temperatuuriväärtusi.
    - Iga sisestusega lisatakse ka valguse andmepunkt.
    - Kuvatakse trendid ja soovitused.
    - Võimalus vaadata statistikat, salvestada ja laadida andmeid.
    
    Ilma niiskuse andmeteta, lihtsustatud.
    """
    global temperature_data, light_data
    global entry_temp
    global label_status, label_temp_trend, label_light_trend, label_suggestions
    global listbox_temp, listbox_light

    # Algandmed
    temperature_data = []
    light_data = []

    root = tk.Tk()
    root.title("Tark Energiasäästja (lihtsustatud)")

    # Menüü salvestamiseks ja laadimiseks
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Salvesta andmed", command=save_data)
    filemenu.add_command(label="Lae andmed", command=load_data)
    menubar.add_cascade(label="Fail", menu=filemenu)
    root.config(menu=menubar)

    frame_input = tk.Frame(root)
    frame_input.pack(pady=10)

    tk.Label(frame_input, text="Sisesta temperatuur (°C):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    entry_temp = tk.Entry(frame_input)
    entry_temp.grid(row=0, column=1, padx=5, pady=5)

    btn_add = tk.Button(frame_input, text="Lisa andmed", command=add_data)
    btn_add.grid(row=0, column=2, padx=5, pady=5)

    label_status = tk.Label(root, text="")
    label_status.pack(pady=5)

    frame_trends = tk.Frame(root)
    frame_trends.pack(pady=10)

    label_temp_trend = tk.Label(frame_trends, text="Temperatuuri trend: Puudub")
    label_temp_trend.pack(side=tk.LEFT, padx=10)

    label_light_trend = tk.Label(frame_trends, text="Valguse trend: Puudub")
    label_light_trend.pack(side=tk.LEFT, padx=10)

    frame_data = tk.Frame(root)
    frame_data.pack(pady=10)

    # Temperatuur
    frame_temp = tk.Frame(frame_data)
    frame_temp.pack(side=tk.LEFT, padx=10)
    tk.Label(frame_temp, text="Temperatuuri andmed:").pack()
    listbox_temp = tk.Listbox(frame_temp, width=20, height=8)
    listbox_temp.pack(pady=5)

    # Valgus
    frame_light = tk.Frame(frame_data)
    frame_light.pack(side=tk.LEFT, padx=10)
    tk.Label(frame_light, text="Valguse andmed:").pack()
    listbox_light = tk.Listbox(frame_light, width=20, height=8)
    listbox_light.pack(pady=5)

    label_suggestions = tk.Label(root, text="Soovitused: ")
    label_suggestions.pack(pady=10)

    btn_stats = tk.Button(root, text="Vaata statistikat", command=show_statistics)
    btn_stats.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
