import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge('/Users/Mohamed/Downloads/msedgedriver')
driver.get('https://web.whatsapp.com/')  # opens whatsapp in the browser
input("Press any key to continue")  # do this after scanning qr code with your phone


def file_write(contact_name, received_message, sent_message):
    f = open("replies.txt", "a")
    t = datetime.datetime.now()
    f.write("replied to <" + contact_name + ">'s: <" + received_message
            + "> " + "with:<" + sent_message + "> " + " at <" + t.strftime(
        "%Y-%m-%d %H:%M:%S>") + "\n")
    f.close()


def spam():
    name = input("contact:")
    contact = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
    contact.click()
    msgBox = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
    song = """sh sh sh sh sh sh sh"""
    song = song.split()
    for i in range(len(song)):
        msgBox.send_keys(song[i])
        sendButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]')
        sendButton.click()


def auto_reply():
    contact_name = ""
    last_message = dict()  # store last message of each chat
    current = 0
    start_time = time.time()
    auto_reply_count = dict()  # counts how many times we replied to each chat
    message_to_be_sent = "test"
    while time.time() - start_time < 28800:  # runs for 8 hours
        contacts = driver.find_elements(By.CLASS_NAME, "_1C6Zl")  # fetches last 15 chats(reads 15 max)
        try:
            contacts[current].click()  # tries to open the chat of current contact
        except:
            print("ERRORRRRR")
        current += 1  # to watch all 15 chats
        if current == len(contacts):  # resets count so that it starts from first chat if it exceeds chat count
            current = 0
        print("watching " + driver.find_element_by_class_name("YEe1t").text + "...")
        msgBox = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')  # fetches the text box we type a message into
        chat_messages = driver.find_elements(By.CLASS_NAME, "_1wlJG")  # fetches current chat messages
        if driver.find_element_by_class_name(
                "YEe1t").text != contact_name:  # if you start watching a different chat,do this
            contact_name = driver.find_element_by_class_name("YEe1t").text  # update contact currently being watched
            if contact_name not in last_message.keys():  # if it's the first time we watch this chat,initialize it's info
                if not len(chat_messages):  # avoid errors
                    continue
                last_message[contact_name] = chat_messages[-1].text  # stores last message in chat
                auto_reply_count[contact_name] = 0
                if time.time() - start_time > 20:  # if a new chat is being watched,and 20 seconds have passed it means this chat is new,so send it a message
                    msgBox.send_keys(
                        message_to_be_sent)  # sends message we want to send to the text box we type a message into
                    last_message[contact_name] = message_to_be_sent  # updates current last message in chat
                    sendButton = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]')
                    if contact_name=="Test5" or contact_name=="Test4" or contact_name=="Test3" or contact_name=="Test2" or contact_name=="Test":
                        sendButton.click()  # clicks the send button for the message to be sent
                    file_write(contact_name, chat_messages[-1].text, message_to_be_sent)
                    continue
        print("All last messages:{}".format(last_message))  # prints last message of every watched chat
        print("{} last message:{}".format(contact_name,
                                          last_message[contact_name]))  # prints last message of currently watched chat
        chat_messages = driver.find_elements(By.CLASS_NAME, "_1wlJG")
        print("comparing: " + chat_messages[-1].text + " and " + last_message[contact_name])
        if chat_messages[-1].text != last_message[
            contact_name]:  # if last stored message is different than the current last message in chat
            if auto_reply_count[contact_name] > 4:  # if you replied to this chat 5 times,don't reply again
                continue
            msgBox.send_keys(message_to_be_sent)
            sendButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]')
            if contact_name == "Test5" or contact_name == "Test4" or contact_name == "Test3" or contact_name == "Test2" or contact_name == "Test":
                sendButton.click()
            last_message[contact_name] = message_to_be_sent  # send message and update last message sent
            auto_reply_count[contact_name] += 1
            file_write(contact_name, chat_messages[-1].text, message_to_be_sent)


auto_reply()
# spam()
