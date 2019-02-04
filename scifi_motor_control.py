#For GUI Creation
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
#For Interfacing with Serial port
import serial, time
import serial.tools.list_ports as port_list
import binascii

class Application(tk.Frame):
    ser = serial.Serial()

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.connect_port()
        self.configure()
        self.get_positions()

    def update_motion_text(self):
        global motion_enabled
        global motion_status
        motion_enabled.set(motion_status)

    def update_position_text(self):
        global left_pos
        global right_pos

        header_string_l = "Position of Left Motor: "
        if limit_list[0] == "Unknown" or limit_list[1] == "Unknown": left_pos.set(header_string_l + "Unknown")
        if limit_list[0] == "engaged" and limit_list[1] == "disengaged": left_pos.set(header_string_l + "Home")
        if limit_list[0] == "disengaged" and limit_list[1] == "engaged": left_pos.set(header_string_l + "Inserted")
        if limit_list[0] == "disengaged" and limit_list[1] == "disengaged": left_pos.set(header_string_l + "Travelling")
       
        header_string_r = "Position of Right Motor: "
        if limit_list[2] == "Unknown" or limit_list[3] == "Unknown": right_pos.set(header_string_r + "Unknown")
        if limit_list[2] == "engaged" and limit_list[3] == "disengaged": right_pos.set(header_string_r + "Home")
        if limit_list[2] == "disengaged" and limit_list[3] == "engaged": right_pos.set(header_string_r + "Inserted")
        if limit_list[2] == "disengaged" and limit_list[3] == "disengaged": right_pos.set(header_string_r + "Travelling")

    def create_widgets(self):

        #adding tab control and two tabs which widgets can be added to
        tabControl = ttk.Notebook(self)

################################################################################

        #adding a menu bar and other elements to access from it
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        comport = Menu(menu)
        comport.add_command(label='Connect COM port', command=self.connect_port)
        menu.add_cascade(label='COMPORT', menu=comport)

        motor = Menu(menu)
        motor.add_command(label='Set Motor/Limits/Velocity', command=self.configure)
        menu.add_cascade(label='Motor', menu=motor)

################################################################################

        #Motor Selection
        self.motor1option = Radiobutton(self, text="Left Motor", variable=var, value = 1, command=self.motor_select)
        self.motor1option.config(state=DISABLED)
        self.motor1option.pack(padx=5, pady=5)
        self.motor2option = Radiobutton(self, text="Right Motor", variable=var, value = 2, command=self.motor_select)
        self.motor2option.config(state=DISABLED)
        self.motor2option.pack(padx=5, pady=5)

        #Move to Home Limit
        self.homepos = tk.Button(self)
        self.homepos["text"] = "Home Limit(+)"
        self.homepos["command"] = self.move_home
        self.homepos.config(state=DISABLED)
        self.homepos.pack(padx=5, pady=5)

        #Move to Far Limit
        self.farlimit = tk.Button(self)
        self.farlimit["text"] = "Far Limit(-)"
        self.farlimit["command"] = self.move_far
        self.farlimit.config(state=DISABLED)
        self.farlimit.pack(padx=5, pady=5)

        #Kill Motion Button
        self.killmotion = tk.Button(self)
        self.killmotion["text"] = "Kill Motion"
        self.killmotion["command"] = self.kill_movement
        self.killmotion.config(state=DISABLED)
        self.killmotion.pack(padx=5, pady=5)
        
        #Get Current Motor Status Button
        self.getpositions = tk.Button(self)
        self.getpositions["text"] = "Get Positions"
        self.getpositions["command"] = self.get_positions
        self.getpositions.pack(padx=5, pady=5)

        #Motor position display
        global left_pos
        global right_pos
        self.update_position_text()
 
        left_position = Label(self, textvariable = left_pos)
        left_position.pack()
        right_position = Label(self, textvariable = right_pos)
        right_position.pack()
        
        #Enable/Disable Motion Button
        self.enablemotion = tk.Button(self)
        self.enablemotion["text"] = "Enable/Disable Motion"
        self.enablemotion["command"] = self.toggle_motion
        self.enablemotion.pack(padx=5, pady=5)
       
        #Motor position display
        global motion_enabled
        self.update_motion_text() 
        motion_enabled_disabled = Label(self, textvariable = motion_enabled)
        motion_enabled_disabled.pack()

################################################################################

    #Below are blocks of code assoicated with each of the features in the GUI

################################################################################

    #Definitions associated with menu bar
    def client_exit(self):
        exit()

    def show_ports(self):
        ports = list(port_list.comports())
        for p in ports:
            print (p)

    def connect_port(self):
        Application.ser.port = '/dev/ttyUSB0' #CHANGE THIS LINE DEPENDING ON THE COMPORT OF YOUR COMPUTER
        Application.ser.baudrate = 9600
        Application.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        Application.ser.parity = serial.PARITY_NONE #set parity check: no parity
        Application.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        Application.ser.timeout = 2              #timeout block read
        Application.ser.xonxoff = False     #disable software flow control
        Application.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        Application.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        Application.ser.writeTimeout = 2     #timeout for write

        try:
            Application.ser.open()

        except Exception as e:
            print("error open serial port: " + str(e))
            exit()

        if Application.ser.isOpen():
            print("succeeded in connecting");
        else:
            print("cannot open serial port ")

    def configure(self):
        try:
            Application.ser.write('F,C,setM1M2,setM2M2,setL1M0,setL2M0,S1M1000,S2M1000'.encode())
            print('Motor #2 for Axis 1 and 2, Limits set to closed to run, Velocity set to 1000 steps/s')
        except:
            print("An error occurred, are you connected to the controller?")

################################################################################

    #Definitions associated with Main Tab of GUI
    def motor_select(self):
        pass

    def move_home(self):
        try:
            MI = str(var.get())
            if MI != "1" and MI != "2":
                print ("An error occurred, you must select a motor!")
                return
            print ("Trying to move motor ",MI)
            command_string = 'F,C,I' + MI + 'M0,I' + MI + 'M-5000,I' + MI + 'M0,R'
            command_byte = command_string.encode()
            time.sleep(0.5)
            Application.ser.write(command_byte)
            #Call limit_status function
            reached_limit = False
            if MI == "1":  
                limit_list[0] = "disengaged"
                limit_list[1] = "disengaged"
            if MI == "2":  
                limit_list[2] = "disengaged"
                limit_list[3] = "disengaged"
            self.update_position_text()
            while not reached_limit:
                time.sleep(0.5)
                # read limit switch
                self.check_limit()
                time.sleep(0.5)
                if MI == "1": print ("limit_list[0] = ",limit_list[0])
                if MI == "2": print ("limit_list[2] = ",limit_list[2])
                if MI == "1" and limit_list[0] == "engaged":
                    reached_limit = True
                if MI == "2" and limit_list[2] == "engaged":
                    reached_limit = True
            print ("Finished moving home")
            self.update_position_text()
        except:
            print("An error occurred, are you connected to the controller?")

    def move_far(self):
        try:
            MI = str(var.get())
            print ("Trying to move motor ",MI)
            command_string = 'F,C,I' + MI + 'M-0,I' + MI + 'M5000,I' + MI + 'M-0,R'
            command_byte = command_string.encode()
            time.sleep(0.5)
            Application.ser.write(command_byte)
            #Call limit_status function
            reached_limit = False
            if MI == "1":  
                limit_list[0] = "disengaged"
                limit_list[1] = "disengaged"
            if MI == "2":  
                limit_list[2] = "disengaged"
                limit_list[3] = "disengaged"
            self.update_position_text()
            while not reached_limit:
                time.sleep(0.5)
                # read limit switch
                self.check_limit()
                time.sleep(0.5)
                if MI == "1": print ("limit_list[1] = ",limit_list[1])
                if MI == "2": print ("limit_list[3] = ",limit_list[3])
                if MI == "1" and limit_list[1] == "engaged":
                    reached_limit = True
                if MI == "2" and limit_list[3] == "engaged":
                    reached_limit = True
            print ("Finished moving in!")
            self.update_position_text()
        except:
            print("An error occurred, are you connected to the controller?")
    
    def get_positions(self):
        global limit_list
        try:
            reached_limit = False
            limit_list = ["Unknown","Unknown","Unknown","Unknown"]
            while not reached_limit:
                time.sleep(0.5)
                self.check_limit()
                time.sleep(0.5)
                print ("limit_list[0] = ",limit_list[0])
                print ("limit_list[1] = ",limit_list[1])
                print ("limit_list[2] = ",limit_list[2])
                print ("limit_list[3] = ",limit_list[3])
                if limit_list[0] != "Unknown" and limit_list[1] != "Unknown" and limit_list[2] != "Unknown" and limit_list[3] != "Unknown":
                    reached_limit = True
            print ("Finished getting positions")
            self.update_position_text()
        except:
            print("An error occurred, are you connected to the controller?")

    def kill_movement(self):
        try:
            command = 'K'
            Application.ser.write(command.encode())
            print('Motion Aborted')
        except:
            pass
    
    def toggle_motion(self):
        try:
            global motion_status
            print ("current motion status = ",motion_status)
            if motion_status == "Disabled":
                password = simpledialog.askstring("Password","Enter password:",show='*')
                if password == "hallA.rocks":
                    motion_status = "Enabled"
                else:
                    print ("Incorrect password!")
                    motion_status = "Disabled"
            else:
                motion_status = "Disabled"
            print ("Updated motion status to ",motion_status) 
            print ("calling update_motion_text()")
            if motion_status == "Enabled":
                self.motor1option.config(state=NORMAL)
                self.motor2option.config(state=NORMAL)
                self.homepos.config(state=NORMAL)
                self.farlimit.config(state=NORMAL)
                self.killmotion.config(state=NORMAL)
            else:
                self.motor1option.config(state=DISABLED)
                self.motor2option.config(state=DISABLED)
                self.homepos.config(state=DISABLED)
                self.farlimit.config(state=DISABLED)
                self.killmotion.config(state=DISABLED)

            self.update_motion_text()
        except:
            pass

################################################################################

    def check_limit(self):
        time.sleep(0.5)
        command = 'F,C,?,R'
        Application.ser.write(command.encode())
        time.sleep(0.5)
        #limit_status = Application.ser.readline()
        limit_status = Application.ser.read()
        time.sleep(0.5)
        print ("Limit status byte= ",limit_status)
        status = limit_status.decode()
        #print ("Status string =",status)
        if status != "":
            bitsnozero = bin(int(binascii.hexlify(status.encode('utf-8','surrogatepass')),16))[2:]
            bits = bitsnozero.zfill(4*((len(bitsnozero)+3)//4))
            print ("Bits =",bits)
            if bits == "1010" or bits == "0010" or bits == "0110" or bits == "1001" or bits == "0001" or bits == "0101" or bits == "1000" or bits == "0000" or bits == "0100":
                status_bits = bits
            else:
                status_bits = "control"
        else:
                status_bits = "control"

        print ("status_bits = ...",status_bits,"...")
        global limit_list

        #print (status_bits[0:1])
        #print (status_bits[1:2])
        #print (status_bits[2:3])
        #print (status_bits[3:4])

        if status_bits[0:1] == "1":
            limit_list[2] = "engaged"
        elif status_bits[0:1] == "0":
            limit_list[2] = "disengaged"
        if status_bits[1:2] == "1":
            limit_list[3] = "engaged"
        elif status_bits[1:2] == "0":
            limit_list[3] = "disengaged"
        if status_bits[2:3] == "1":
            limit_list[0] = "engaged"
        elif status_bits[2:3] == "0":
            limit_list[0] = "disengaged"
        if status_bits[3:4] == "1":
            limit_list[1] = "engaged"
        elif status_bits[3:4] == "0":
            limit_list[1] = "disengaged"

        print (limit_list)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SciFi Motor Control")
    root.geometry("250x340")
    
    var = IntVar()
    left_pos = StringVar()
    right_pos = StringVar()
    motion_enabled = StringVar()

    limit_list = ['Unknown','Unknown','Unknown','Unknown']
    motion_status = "Disabled"

    main = Application(root)
    root.mainloop()
