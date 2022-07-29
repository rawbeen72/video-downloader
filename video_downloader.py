from datetime import datetime
import urllib.request
import pyperclip
import sys
import time
from PyQt5.QtWidgets import QDialog, QApplication
import pyperclip
from demo_fb import *
from selenium.webdriver.common.action_chains import ActionChains
import requests
from selenium import webdriver
import re
import threading
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

from getpass import getuser
username = getuser()
chrome_options = Options()
headers = headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
now = str(datetime.now())
now = now[0:19]
now = now.replace(":", "-")
file_location = f"C:\\Users\\acer\\Downloads\\{now}"+'.mp4'


class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButtonDownload.clicked.connect(self.big_thread)
        # self.ui.horizontalSlider.valueChanged.connect(self.change_themes)

    def big_thread(self):
        th = threading.Thread(target=self.download_video)
        th.start()

    def download_video(self):
        global file_location
        self.ui.labelWarning.clear()
        url_text = self.ui.lineEditURL.text()
        try:
            if "facebook.com" in url_text:
                self.ui.labelWarning.setText("facebook url detected")
                self.ui.labelProgressBar.clear()

                if ", " in url_text:
                    url_lst = url_text.split(", ")
                    for i in url_lst:
                        self.ui.labelWarning.setText("facebook url detected")
                        url = requests.get(i, headers=headers)
                        video_url = re.search(
                            '_src:"(.+?)"', url.content.decode('utf-8')).group(1)

                        # self.ui.labelWarning.clear()
                        file_location = file_location
                        self.ui.labelProgressBar.setText(
                            "Downloading video...")

                        urllib.request.urlretrieve(
                            video_url, file_location, self.Handle_Progress)
                        self.ui.labelProgressBar.setText(
                            "Video(s) downloaded successfully :)")
                        self.ui.labelWarning.clear()

                else:
                    url = requests.get(url_text, headers=headers)
                    video_url = re.search(
                        '_src:"(.+?)"', url.content.decode('utf-8')).group(1)
                    # print(video_url)

                    # print(video_url)
                    # print(type(video_url))
                    self.ui.labelWarning.clear()
                    file_location = file_location
                    self.ui.labelProgressBar.setText("Downloading video...")

                    urllib.request.urlretrieve(
                        video_url, file_location, self.Handle_Progress)
                    self.ui.labelProgressBar.setText(
                        "Video(s) downloaded successfully :)")
                    self.ui.labelWarning.clear()

            elif "youtube.com" in url_text or "youtu.be" in url_text:
                self.ui.labelWarning.setText("Youtube url detected")
                yt_url = url_text
                # if "youtu.be" in yt_url:
                try:
                    yt_url = yt_url.replace(
                        "youtu.be/", "www.youtube.com/watch?v=")
                    # print(yt_url)
                except Exception as e:
                    print(e)

                if ", " in yt_url:
                    self.ui.labelProgressBar.clear()
                    self.ui.labelProgressBar.setText("Downloading video...")

                    yt_url = yt_url.replace("youtube", "clipmega")
                    url_lst = yt_url.split(", ")
                    for i in url_lst:
                        url = requests.get(i, headers=headers)
                        soup = BeautifulSoup(url.text, "html.parser")
                        link = soup.select(".btn-group > a")
                        link = link[0]
                        link = str(link)
                        indx = link.find("href=")
                        indx_l = link.find("extension=mp4")
                        link = link[indx+6:indx_l+13].replace("amp;", "")
                        link = link.replace(" ", "%20")
                        final_link = link

                        file_location = file_location
                        try:
                            self.ui.labelProgressBar.setText(
                                "Downloading video...")
                            urllib.request.urlretrieve(
                                final_link, file_location, self.Handle_Progress)
                            self.ui.labelProgressBar.setText(
                                "Video(s) downloaded successfully :)")
                            self.ui.labelWarning.clear()

                        except Exception as e:
                            self.ui.labelWarning.setText("Error: " + str(e))
                else:
                    yt_url = yt_url.replace("youtube", "clipmega")
                    url = requests.get(yt_url, headers=headers)
                    soup = BeautifulSoup(url.text, "html.parser")
                    link = soup.select(".btn-group > a")
                    link = link[0]
                    link = str(link)
                    indx = link.find("href=")
                    indx_l = link.find("extension=mp4")
                    link = link[indx+6:indx_l+13].replace("amp;", "")
                    link = link.replace(" ", "%20")
                    final_link = link

                    file_location = file_location
                    try:
                        self.ui.labelProgressBar.setText(
                            "Downloading video...")
                        urllib.request.urlretrieve(
                            final_link, file_location, self.Handle_Progress)
                        self.ui.labelWarning.clear()
                        self.ui.labelProgressBar.setText(
                            "Video(s) downloaded successfully :)")
                        self.ui.labelWarning.clear()

                    except Exception as e:
                        self.ui.labelWarning.setText("Error: " + str(e))

            else:
                final_link = self.ui.lineEditURL.text()
                print(final_link)
                opener = urllib.request.build_opener()

                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                try:
                    self.ui.labelProgressBar.setText(
                        "Downloading video...")
                    urllib.request.urlretrieve(
                        final_link, file_location, self.Handle_Progress)
                    self.ui.labelWarning.clear()
                    self.ui.labelProgressBar.setText(
                        "Video(s) downloaded successfully :)")
                    self.ui.labelWarning.clear()

                except Exception as e:
                    self.ui.labelWarning.setText("Error: " + str(e))

        except Exception as e:
            self.ui.labelWarning.setText("Error: " + str(e))

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        readed_data = blocknum * blocksize
        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.ui.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    # def change_themes(self):
    #     slider = self.ui.horizontalSlider.value()
    #     if slider > 0 and slider < 15:
    #         sshFile = r"F:\Python\NEW PYQT5\Obit.txt"
    #         with open(sshFile, "r") as fh:
    #             self.setStyleSheet(fh.read())
    #     if slider > 15 and slider < 35:
    #         sshFile = r"F:\Python\NEW PYQT5\Irrorater.txt"
    #         with open(sshFile, "r") as fh:
    #             self.setStyleSheet(fh.read())
    #     if slider > 35 and slider < 50:
    #         sshFile = r"F:\Python\NEW PYQT5\Hookmark.txt"
    #         with open(sshFile, "r") as fh:
    #             self.setStyleSheet(fh.read())
    #     if slider > 50 and slider < 65:
    #         sshFile = r"F:\Python\NEW PYQT5\Incrypt.txt"
    #         with open(sshFile, "r") as fh:
    #             self.setStyleSheet(fh.read())

    #     if slider > 65 and slider < 80:
    #         sshFile = r"F:\Python\NEW PYQT5\Obit.txt"
    #         with open(sshFile, "r") as fh:
    #             self.setStyleSheet(fh.read())
    #     if slider > 80 and slider <= 99:
    #         sshFile = r"F:\Python\NEW PYQT5\SyNet.txt"
    #         with open(sshFile, "r") as fh:
    #             self.setStyleSheet(fh.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
