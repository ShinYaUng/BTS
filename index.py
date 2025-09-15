import tkinter as tk
from tkinter import Toplevel

class TicketSystem:
    def __init__(self):
        self.stations = ["Station A", "Station B", "Station C", "Station D", "Station E", "Station F", "Station G"]
        self.base_price = 15  # ราคาพื้นฐานต่อสถานี
        self.sales_records = []  # เก็บรายรับ, เงินทอน และราคาตั๋วในรูปแบบ list

    def calculate_price(self, start_station, end_station):
        start_index = self.stations.index(start_station)
        end_index = self.stations.index(end_station)
        distance = abs(end_index - start_index)  # คำนวณระยะทางตามจำนวนสถานี
        price_per_ticket = self.base_price * distance
        return price_per_ticket

    def calculate_change(self, change):
        """คำนวณการทอนเงินเป็นเหรียญ"""
        coins = [10, 5, 2, 1]
        change_distribution = {}
        for coin in coins:
            coin_count = int(change // coin)
            if coin_count > 0:
                change_distribution[coin] = coin_count
            change = round(change % coin, 2)
        return change_distribution

    def buy_ticket(self, start_station, end_station, amount_paid, ticket_count):
        price_per_ticket = self.calculate_price(start_station, end_station)
        total_price = price_per_ticket * ticket_count
        
        if total_price == 0:
            return "เส้นทางไม่ถูกต้อง", None, None
        if amount_paid < total_price:
            return "เงินไม่พอ", None, None
        change = amount_paid - total_price
        
        # เก็บข้อมูลการขาย (เพิ่มจำนวนตั๋วและเงินที่ได้รับ)
        self.sales_records.append((start_station, end_station, price_per_ticket, ticket_count, amount_paid, total_price, change))
        
        # คำนวณการทอนเป็นเหรียญ
        change_distribution = self.calculate_change(change)

        # บันทึกลงไฟล์
        self.save_to_file(start_station, end_station, price_per_ticket, ticket_count, amount_paid, total_price, change)
        
        return "ซื้อสำเร็จ", change, change_distribution

    def save_to_file(self, start_station, end_station, price_per_ticket, ticket_count, amount_paid, total_price, change):
        """บันทึกสถิติการขายลงในไฟล์ text พร้อมราคาตั๋ว จำนวนตั๋ว เงินที่ได้รับ รายรับ และเงินทอน"""
        with open("ticket_sales.txt", "a", encoding="utf-8") as file:
            file.write(f"สถานีต้นทาง: {start_station}, สถานีปลายทาง: {end_station}, ราคาตั๋ว: {price_per_ticket} บาท, "
                       f"จำนวนตั๋ว: {ticket_count}, เงินที่ได้รับ: {amount_paid} บาท, รายรับ: {total_price} บาท, "
                       f"เงินทอน: {change:.2f} บาท\n")

class TicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ระบบขายตั๋วรถไฟ")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f8ff")  # เปลี่ยนสีพื้นหลัง

        self.system = TicketSystem()

        # ใช้ฟอนต์ที่ชัดเจนและปรับขนาด
        self.custom_font = ("Helvetica", 15)

        # สร้าง GUI Components
        self.label_title = tk.Label(root, text="ระบบขายตั๋วรถไฟ", font=("Helvetica", 16, "bold"), bg="#f0f8ff")
        self.label_title.pack(pady=10)

        self.label_start = tk.Label(root, text="สถานีต้นทาง:", font=self.custom_font, bg="#f0f8ff")
        self.label_start.pack()

        self.start_station_var = tk.StringVar(value=self.system.stations[0])
        self.start_station_menu = tk.OptionMenu(root, self.start_station_var, *self.system.stations, command=self.update_price)
        self.start_station_menu.config(font=self.custom_font)
        self.start_station_menu.pack()

        self.label_end = tk.Label(root, text="สถานีปลายทาง:", font=self.custom_font, bg="#f0f8ff")
        self.label_end.pack()

        self.end_station_var = tk.StringVar(value=self.system.stations[1])
        self.end_station_menu = tk.OptionMenu(root, self.end_station_var, *self.system.stations, command=self.update_price)
        self.end_station_menu.config(font=self.custom_font)
        self.end_station_menu.pack()

        # เลือกจำนวนตั๋ว
        self.label_ticket_count = tk.Label(root, text="จำนวนตั๋ว:", font=self.custom_font, bg="#f0f8ff")
        self.label_ticket_count.pack()

        self.ticket_count_var = tk.IntVar(value=1)
        self.ticket_count_spinbox = tk.Spinbox(root, from_=1, to=5, font=self.custom_font, textvariable=self.ticket_count_var, command=self.update_price)
        self.ticket_count_spinbox.pack(pady=5)

        self.label_price = tk.Label(root, text="ราคาตั๋ว: 0 บาท", font=self.custom_font, bg="#f0f8ff")
        self.label_price.pack(pady=10)

        self.label_amount = tk.Label(root, text="จำนวนเงินที่จ่าย:", font=self.custom_font, bg="#f0f8ff")
        self.label_amount.pack()

        self.entry_amount = tk.Entry(root, font=self.custom_font)
        self.entry_amount.pack(pady=5)

        self.buy_button = tk.Button(root, text="ซื้อ", font=("Helvetica", 12, "bold"), bg="#4682b4", fg="white", command=self.buy_ticket)
        self.buy_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=self.custom_font, bg="#f0f8ff")
        self.result_label.pack(pady=5)

        # ปุ่มแสดงสถิติการขาย
        self.stats_button = tk.Button(root, text="แสดงสถิติการขาย", font=("Helvetica", 12), bg="#4682b4", fg="white", command=self.show_stats)
        self.stats_button.pack(pady=5)

    def update_price(self, *args):
        """อัปเดตราคาตามสถานีที่เลือกและจำนวนตั๋ว"""
        start_station = self.start_station_var.get()
        end_station = self.end_station_var.get()
        ticket_count = self.ticket_count_var.get()
        price_per_ticket = self.system.calculate_price(start_station, end_station)
        total_price = price_per_ticket * int(ticket_count)
        self.label_price.config(text=f"ราคาตั๋ว: {total_price} บาท")

    def buy_ticket(self):
        start_station = self.start_station_var.get()
        end_station = self.end_station_var.get()
        ticket_count = int(self.ticket_count_var.get())
        try:
            amount_paid = float(self.entry_amount.get())
        except ValueError:
            self.show_large_messagebox("ข้อผิดพลาด", "กรุณากรอกจำนวนเงินที่ถูกต้อง")
            return

        result, change, change_distribution = self.system.buy_ticket(start_station, end_station, amount_paid, ticket_count)
        if change is not None:
            # แสดงผลการทอนเหรียญ
            change_details = ", ".join([f"เหรียญ {coin} บาท {count} เหรียญ" for coin, count in change_distribution.items()])
            self.result_label.config(text=f"{result}. เงินทอน: {change:.2f} บาท ({change_details})")
        else:
            self.result_label.config(text=result)

    def show_large_messagebox(self, title, message):
        """สร้าง messagebox ขนาดใหญ่โดยใช้ Toplevel"""
        top = Toplevel(self.root)
        top.title(title)
        top.geometry("600x400")  # กำหนดขนาดให้ใหญ่ขึ้น
        top.config(bg="#f0f8ff")

        # สร้าง Text widget แทน Label เพื่อแสดงข้อความที่มีรูปแบบ
        text_box = tk.Text(top, wrap='word', font=("Helvetica", 12), bg="#f0f8ff", fg="black")
        text_box.pack(expand=True, fill='both', padx=10, pady=10)

        # แทรกข้อความใน Text widget
        text_box.insert(tk.END, message)
        text_box.config(state=tk.DISABLED)  # ปิดการแก้ไข Text widget

        button_close = tk.Button(top, text="ปิด", command=top.destroy, bg="#4682b4", fg="white", font=("Helvetica", 12, "bold"))
        button_close.pack(pady=10)

    def show_stats(self):
        """แสดงสถิติการขาย"""
        stats = "\n".join([f"จาก {start} ไป {end}:\n"
                           f"  ราคาตั๋ว: {price} บาท\n"
                           f"  จำนวนตั๋ว: {count}\n"
                           f"  เงินที่ได้รับ: {paid} บาท\n"
                           f"  รายรับ: {total} บาท\n"
                           f"  เงินทอน: {change:.2f} บาท\n"
                           f"{'-'*30}"  # เพิ่มเส้นแบ่งระหว่างรายการ
                           for start, end, price, count, paid, total, change in self.system.sales_records])

        if stats:
            self.show_large_messagebox("สถิติการขาย", f"สถิติการขาย:\n\n{stats}")
        else:
            self.show_large_messagebox("สถิติการขาย", "ยังไม่มีข้อมูลการขาย")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketApp(root)
    root.mainloop()