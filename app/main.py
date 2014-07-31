from mail import mail
from crypto import crypto
from threading import Thread

if __name__ == '__main__':
    encryption = crypto.crypto()
    
    encrypted = encryption.encrypt('payload', True)
    print('encrypted \t' + encrypted)
    
    decrypted = encryption.decrypt(encrypted, True)
    print('decrypted \t' + decrypted)
    
    mail = mail.mail()    
    thread = Thread(target = mail.send_forgot_password, args = ("garydavidwilliams@gmail.com", encrypted, ))
    thread.start()
    thread.join()
    
    #mail.send_forgot_password("garydavidwilliams@gmail.com", encrypted)
