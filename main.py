# -*- coding: utf-8 -*-  
"""  
Created on Tue Nov 5 14:41:35 2024  
  
@author: ouyangjiahong  
"""  
  
import tkinter as tk  
from tkinter import simpledialog, messagebox  
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import numpy as np  
  
class OneRMCalculator:  
    def __init__(self, master):  
        self.master = master  
        master.title("1RM Calculator")  
  
        self.label = tk.Label(master, text="Enter Load-Velocity Data:")  
        self.label.pack()  
  
        self.data_entry_frame = tk.Frame(master)  
        self.data_entry_frame.pack()  
  
        self.add_data_button = tk.Button(master, text="Add Data", command=self.add_data_entry)  
        self.add_data_button.pack()  
  
        self.velocity_label = tk.Label(master, text="1RM Velocity (default 0.33):")  
        self.velocity_label.pack()  
  
        self.velocity_entry = tk.Entry(master)  
        self.velocity_entry.insert(0, "0.33")  
        self.velocity_entry.pack()  
  
        self.calculate_button = tk.Button(master, text="Calculate 1RM", command=self.calculate_1rm)  
        self.calculate_button.pack()  
  
        self.result_label = tk.Label(master, text="")  
        self.result_label.pack()  
  
        self.plot_frame = tk.Frame(master)  
        self.plot_frame.pack()  
  
        self.data = {'Load': [], 'Velocity': []}  
        self.data_entries = []  
  
    def add_data_entry(self):  
        # Create a new row for data entry  
        row_frame = tk.Frame(self.data_entry_frame)  
        load_entry = tk.Entry(row_frame)  
        load_entry.grid(row=0, column=0)  
        velocity_entry = tk.Entry(row_frame)  
        velocity_entry.grid(row=0, column=1)  
        delete_button = tk.Button(row_frame, text="Delete", command=lambda: self.delete_data_entry(row_frame))  
        delete_button.grid(row=0, column=2)  
        row_frame.pack()  
  
        # Store the entries in a list for later retrieval  
        self.data_entries.append((load_entry, velocity_entry))  
  
    def delete_data_entry(self, row_frame):  
        # Remove the row_frame from the data_entry_frame  
        row_frame.destroy()  
        # Remove the corresponding entries from the data_entries list  
        self.data_entries = [(load_entry, velocity_entry) for (load_entry, velocity_entry), frame in zip(self.data_entries, self.data_entry_frame.winfo_children()) if frame != row_frame]  
  
    def get_data_from_entries(self):  
        # Retrieve data from the entries  
        self.data['Load'] = []  
        self.data['Velocity'] = []  
        for load_entry, velocity_entry in self.data_entries:  
            try:  
                load = float(load_entry.get())  
                velocity = float(velocity_entry.get())  
                self.data['Load'].append(load)  
                self.data['Velocity'].append(velocity)  
            except ValueError:  
                messagebox.showerror("Error", "Please enter valid numbers for all fields")  
                return False  
        return True  
  
    def calculate_1rm(self):  
        if not self.get_data_from_entries():  
            return  
  
        loads = np.array(self.data['Load'])  
        velocities = np.array(self.data['Velocity'])  
  
        if len(loads) < 2:  
            messagebox.showerror("Error", "At least two data points are required to calculate 1RM")  
            return  
  
        # Perform linear regression to get the trend line  
        coefficients = np.polyfit(velocities, loads, 1)  
        a, b = coefficients  # coefficients[0] is a, coefficients[1] is b  
  
        # Get 1RM velocity from entry, default to 0.33 if not provided  
        try:  
            one_rm_velocity = float(self.velocity_entry.get())  
        except ValueError:  
            one_rm_velocity = 0.33  
  
        # Calculate 1RM  
        self.one_rm = a * one_rm_velocity + b  
  
        # Update the plot and result label  
        self.plot_data(coefficients)  
        self.result_label.config(text=f"The calculated 1RM is: {self.one_rm:.2f}\nLinear Fit: Load = {a:.2f} * Velocity + {b:.2f}")  
  
    def plot_data(self, coefficients):  
        # Clear the previous plot if exists  
        for widget in self.plot_frame.winfo_children():  
            widget.destroy()  
  
        fig, ax = plt.subplots()  
        ax.scatter(self.data['Velocity'], self.data['Load'], color='blue')  
        velocity_range = np.linspace(min(self.data['Velocity']), max(self.data['Velocity']), 100)  
        trend_line = coefficients[0] * velocity_range + coefficients[1]  
        ax.plot(velocity_range, trend_line, color='red')  
        ax.set_xlabel('Velocity')  
        ax.set_ylabel('Load')  
        ax.set_title('Load-Velocity Curve')  
  
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)  
        canvas.draw()  
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)  
  
if __name__ == "__main__":  
    root = tk.Tk()  
    app = OneRMCalculator(root)  
    root.mainloop()