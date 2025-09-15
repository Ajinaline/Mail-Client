from PyQt5.QtWidgets import *
from PyQt5 import uic

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class MyGUI(QMainWindow):
    
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("mailgui.ui", self)
        self.show()
        
        self.loginbutt.clicked.connect(self.login)
        self.attachbutt.clicked.connect(self.attach_sth)
        self.sendbutt.clicked.connect(self.send_mail)
        
    def login(self):
        try:
            self.server = smtplib.SMTP(self.serverline.text(), self.portline.text())
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.addressline.text(), self.passwordline.text())
            
            self.addressline.setEnabled(False)
            self.passwordline.setEnabled(False)
            self.serverline.setEnabled(False)
            self.portline.setEnabled(False)
            self.loginbutt.setEnabled(False)
            
            self.toline.setEnabled(True)
            self.subjectline.setEnabled(True)
            self.yapline.setEnabled(True)
            self.attachbutt.setEnabled(True)
            self.sendbutt.setEnabled(True)
            
            self.msg = MIMEMultipart()
        except smtplib.SMTPAuthenticationError:
            QMessageBox.warning(self, "Error", "Invalid email or password.")
        except smtplib.SMTPConnectError:
            QMessageBox.warning(self, "Error", "Failed to connect to the SMTP server. Check the server address and port.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
    
    def attach_sth(self):
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "All Files (*.*)", options=options)
        if filenames != []:
            for filename in filenames:
                attachment = open(filename, "rb")
                
                filename = filename[filename.rfind("/") + 1:]
                
                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header("Content-Disposition", f"attachment; filename={filename}")
                self.msg.attach(p)
                if not self.label_8.text().endswith(":"):
                    self.label_8.setText(self.label_8.text() + ",")
                self.label_8.setText(self.label_8.text() + " " + filename)
    
    def send_mail(self):
        dialog = QMessageBox()
        dialog.setText("Do you want to send this mail?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole)
        
        if dialog.exec_() == 0:
            try:
                self.msg["From"] = self.addressline.text()
                self.msg["To"] = self.toline.text()
                self.msg["Subject"] = self.subjectline.text()
                self.msg.attach(MIMEText(self.yapline.toPlainText(), "plain"))
                text = self.msg.as_string()
                self.server.sendmail(self.addressline.text(), self.toline.text(), text)
                message_box = QMessageBox()
                message_box.setText("Mail sent!")
                message_box.exec()
            except:
                message_box = QMessageBox()
                message_box.setText("Sending mail failed!")
                message_box.exec()
        
app = QApplication([])
window = MyGUI()
app.exec_()