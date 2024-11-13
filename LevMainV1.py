# Algversioon

def main():
    # Create a basic tkinter window
    root = tk.Tk()
    root.title("Tark Energiasäästja")

    # Example data
    temperaturedata = [collect_data("temperature") for  in range(10)]
    lightdata = [collect_data("light") for  in range(10)]

    # Analyze trends
    temperature_trend = analyze_trends(temperature_data)
    light_trend = analyze_trends(light_data)

    # Display in the GUI
    tk.Label(root, text=f"Temperature Trend: {temperature_trend}").pack()
    tk.Label(root, text=f"Light Trend: {light_trend}").pack()

    # Show a simple plot
    plt.plot(temperature_data, label="Temperature")
    plt.plot(light_data, label="Light")
    plt.legend()
    plt.show()

    root.mainloop()
