import tkinter as tk
import threading
import speedtest
import math
import time
import random

class SpeedTestApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Internet Speed Test")
        self.root.geometry("700x950")  
        self.root.config(bg="#1a1a2e")
        self.root.resizable(False, False)
        
        self.testing = False
        self.max_speed = 200  # Mbps
        
        self.setup_ui()
        
    def setup_ui(self):
        #title
        title = tk.Label(self.root, text="Internet Speed Test", 
                        font=("Arial", 32, "bold"), 
                        bg="#1a1a2e", fg="white")
        subtitle = tk.Label(self.root, text="- Jatin Raikwar", 
                        font=("Times New Roman", 16, "bold"), 
                        bg="#1a1a2e", fg="gray")
        title.pack(pady=5)
        subtitle.pack()
        
        #canvas for speedometer
        self.canvas = tk.Canvas(self.root, width=600, height=450, bg="#1a1a2e", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.create_speedometer()
        
        #real-time speed display
        self.speed_display = tk.Label(self.root, text="0.0", 
                                     font=("Arial", 48, "bold"), 
                                     bg="#1a1a2e", fg="#00ff88")
        self.speed_display.pack(pady=5)
        tk.Label(self.root, text="Mbps", font=("Arial", 16), bg="#1a1a2e", fg="gray").pack()
        
        #status label
        self.status_label = tk.Label(self.root, text="Click START to begin test", 
                                    font=("Arial", 14), 
                                    bg="#1a1a2e", fg="white")
        self.status_label.pack(pady=10)
        
        #results frame
        results_frame = tk.Frame(self.root, bg="#1a1a2e")
        results_frame.pack(pady=10)
        
        #ping
        ping_frame = tk.Frame(results_frame, bg="#2d2d44", bd=2, relief="raised")
        ping_frame.grid(row=0, column=0, padx=15, ipadx=20, ipady=15)
        tk.Label(ping_frame, text="PING", font=("Arial", 12, "bold"), bg="#2d2d44", fg="gray").pack()
        self.ping_result = tk.Label(ping_frame, text="--", font=("Arial", 20, "bold"), bg="#2d2d44", fg="white")
        self.ping_result.pack()
        tk.Label(ping_frame, text="ms", font=("Arial", 10), bg="#2d2d44", fg="gray").pack()
        
        #download
        download_frame = tk.Frame(results_frame, bg="#2d2d44", bd=2, relief="raised")
        download_frame.grid(row=0, column=1, padx=15, ipadx=20, ipady=15)
        tk.Label(download_frame, text="DOWNLOAD", font=("Arial", 12, "bold"), bg="#2d2d44", fg="gray").pack()
        self.download_result = tk.Label(download_frame, text="--", font=("Arial", 20, "bold"), bg="#2d2d44", fg="#00ff88")
        self.download_result.pack()
        tk.Label(download_frame, text="Mbps", font=("Arial", 10), bg="#2d2d44", fg="gray").pack()
        
        # Upload
        upload_frame = tk.Frame(results_frame, bg="#2d2d44", bd=2, relief="raised")
        upload_frame.grid(row=0, column=2, padx=15, ipadx=20, ipady=15)
        tk.Label(upload_frame, text="UPLOAD", font=("Arial", 12, "bold"), bg="#2d2d44", fg="gray").pack()
        self.upload_result = tk.Label(upload_frame, text="--", font=("Arial", 20, "bold"), bg="#2d2d44", fg="#ff6b35")
        self.upload_result.pack()
        tk.Label(upload_frame, text="Mbps", font=("Arial", 10), bg="#2d2d44", fg="gray").pack()
        
        #start button
        self.start_button = tk.Button(self.root, 
                                     text="START SPEED TEST", 
                                     font=("Arial", 20, "bold"), 
                                     bg="#00ff88",
                                     fg="black",
                                     width=22, 
                                     height=3,
                                     relief="raised",
                                     bd=3,
                                     cursor="hand2",
                                     command=self.start_test)
        self.start_button.pack(pady=20)
        
    #speedometer
    def create_speedometer(self):
        self.canvas.delete("all")
        cx, cy = 300, 220
        radius = 150
        
        #background semi-circle
        self.canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius, start=135, extent=270, style="arc", width=10, outline="#666")
        
        #tick marks and numbers
        for i in range(0, self.max_speed+1, 25):
            angle = self.speed_to_angle(i)
            x1 = cx + radius * math.cos(math.radians(angle))
            y1 = cy + radius * math.sin(math.radians(angle))
            x2 = cx + (radius-15) * math.cos(math.radians(angle))
            y2 = cy + (radius-15) * math.sin(math.radians(angle))
            self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2)
            
            if i % 50 == 0:
                x_text = cx + (radius+25) * math.cos(math.radians(angle))
                y_text = cy + (radius+25) * math.sin(math.radians(angle))
                self.canvas.create_text(x_text, y_text, text=str(i), fill="white", font=("Arial", 10, "bold"))
        
        #needle
        self.needle = self.canvas.create_line(cx, cy, cx-radius+50, cy-98, fill="#00ff88", width=4)
        #center dot
        self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill="#00ff88", outline="white")
    
    def speed_to_angle(self, speed):
        if speed > self.max_speed:
            speed = self.max_speed
        return 225 - (speed / self.max_speed) * 270
    
    def update_speedometer(self, speed):
        angle = self.speed_to_angle(speed)
        cx, cy = 300, 220
        radius = 150
        x = cx + (radius-2) * math.cos(math.radians(angle))
        y = cy + (radius-5) * math.sin(math.radians(angle))
        self.canvas.coords(self.needle, cx, cy, x, y)
        self.speed_display.config(text=f"{speed:.1f}")
        self.root.update()
    
    def animate_speed(self, target_speed, duration=3.0, test_type="download"):
        steps = 100  
        for i in range(steps+1):
            progress = i / steps
            base_speed = target_speed * progress
            fluctuation = random.uniform(-0.05 * target_speed, 0.05 * target_speed)
            current_speed = max(0, min(base_speed + fluctuation, self.max_speed))
            self.update_speedometer(current_speed)
            time.sleep(duration / steps)
        self.update_speedometer(target_speed)
        
        if test_type == "download":
            self.download_result.config(text=f"{target_speed:.1f}")
        else:
            self.upload_result.config(text=f"{target_speed:.1f}")

    
    #test logic
    def run_test(self):
        try:
            self.status_label.config(text="Connecting to server...")
            st = speedtest.Speedtest()
            self.status_label.config(text="Getting server list...")
            st.get_best_server()
            
            #ping
            self.status_label.config(text="Testing ping...")
            ping = st.results.ping
            self.ping_result.config(text=f"{ping:.0f}")
            time.sleep(1)
            
            #download
            self.status_label.config(text="Testing download speed...")
            download_speed = st.download() / 1_000_000
            self.animate_speed(download_speed, 4.0, "download")
            
            # Reset for upload
            self.update_speedometer(0)
            time.sleep(0.5)
            
            #upload
            self.status_label.config(text="Testing upload speed...")
            upload_speed = st.upload() / 1_000_000
            self.animate_speed(upload_speed, 4.0, "upload")
            
            self.status_label.config(text="Test completed successfully!")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
        finally:
            self.testing = False
            self.start_button.config(state="normal", text="START SPEED TEST", bg="#00ff88")
    
    def start_test(self):
        if self.testing:
            return
        self.testing = True
        self.start_button.config(state="disabled", text="TESTING...", bg="gray")
        # Reset
        self.ping_result.config(text="--")
        self.download_result.config(text="--")
        self.upload_result.config(text="--")
        self.update_speedometer(0)
        threading.Thread(target=self.run_test, daemon=True).start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SpeedTestApp()
    app.run()
