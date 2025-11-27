import socket
import threading
import customtkinter as ctk # Using customtkinter instead of standard tkinter
from tkinter import messagebox
import traceback

# Set appearance mode and default color theme
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Safe Import for Emoji
try:
    import emoji
except ImportError:
    emoji = None 

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        
        # Use CTkInputDialog for modern nickname input
        dialog = ctk.CTkInputDialog(text="Choose a nickname:", title="Welcome")
        self.nickname = dialog.get_input()
        
        if self.nickname:
            self.connect_to_server(host, port)
            self.gui_loop()
        else:
            exit(0)
        
    def connect_to_server(self, host, port):
        try:
            self.sock.connect((host, port))
            self.connected = True
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect: {e}")
            exit(0)

    def gui_loop(self):
        # Main Window Setup
        self.win = ctk.CTk()
        self.win.title(f"LAN Chat Pro - {self.nickname}")
        self.win.geometry("500x600") # Set initial size

        # Use a modern font
        self.font_main = ("Roboto", 14)
        self.font_msg = ("Roboto", 12)

        # 1. Chat Display Area (Using CTkTextbox)
        self.text_area = ctk.CTkTextbox(self.win, font=self.font_msg)
        self.text_area.pack(padx=20, pady=(20, 10), fill="both", expand=True)
        self.text_area.configure(state='disabled')

        # Frame for Input and Button to keep them together
        self.input_frame = ctk.CTkFrame(self.win, fg_color="transparent")
        self.input_frame.pack(padx=20, pady=(0, 20), fill="x")

        # 2. Message Input Box (Using CTkEntry with placeholder)
        self.input_area = ctk.CTkEntry(self.input_frame, 
                                       placeholder_text="Type your message here... (Try :smile:)",
                                       height=40,
                                       font=self.font_main)
        self.input_area.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Bind Enter key to send message
        self.input_area.bind("<Return>", lambda event: self.write())

        
        # 3. Send Button (Modern rounded button)
        self.send_button = ctk.CTkButton(self.input_frame, 
                                         text="Send ➤", 
                                         command=self.write,
                                         height=40,
                                         font=self.font_main)
        self.send_button.pack(side="right")

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        # Thread starts after UI is ready
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        self.win.mainloop()

    def write(self):
        if not self.connected:
            return

        text = self.input_area.get()
        if not text: # Don't send empty messages
            return
            
        if emoji:
            text = emoji.emojize(text)
            
        message = f"{self.nickname}: {text}"
        try:
            self.sock.send(message.encode('utf-8'))
            self.input_area.delete(0, 'end') # Clear input after sending
        except Exception as e:
            print(f"Send Error: {e}")
            self.stop()

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    # Insert message into CTkTextbox
                    self.text_area.configure(state='normal')
                    self.text_area.insert('end', message + '\n\n') # Add double newline for spacing
                    self.text_area.see('end') # Auto-scroll to bottom
                    self.text_area.configure(state='disabled')
            except ConnectionAbortedError:
                break
            except Exception as e:
                print("An error occurred:")
                traceback.print_exc()
                self.sock.close()
                break

    def stop(self):
        self.connected = False
        self.sock.close()
        try:
            self.win.destroy()
        except:
            pass
        exit(0)

if __name__ == "__main__":
    # IMPORTANT: Change this to your REAL IP before creating EXE
    HOST = '172.20.50.192' # Unga pazhaya IP inga podunga
    PORT = 55555
    client = Client(HOST, PORT)