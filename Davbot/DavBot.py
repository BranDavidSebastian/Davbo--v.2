from modelare import *



def centrare():
    centru = QDesktopWidget().availableGeometry().center()

    lungime = centru.x() - 200
    latime = centru.y() - 300

    return lungime,latime




class MainWindow(QMainWindow):

    def  __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.setFixedSize(400, 600)
        x, y = centrare()
        self.setGeometry(x, y,400,600)
        self.setWindowTitle("DavBot")
        oImage = QImage("Img/Backround.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)


    def initUI(self):

        self.button = QPushButton('', self)
        self.button.setGeometry(200, 150, 80, 80)
        self.button.move(300,400)
        # setting radius and border
        self.button.setStyleSheet("border-radius : 40 ;border: 2px solid black; background-image : url(Img/scriere.png);")
        self.button.clicked.connect(self.clicked_Scriere)


        self.button3 = QPushButton('', self)
        self.button3.setGeometry(200, 150, 80, 80)
        self.button3.move(20,400)
        self.button3.setStyleSheet("border-radius : 40 ;border: 2px solid black; background-image : url(Img/voce.png);")

        self.button3.clicked.connect(self.clicked_Vorbire)

        self.button2 = QPushButton('', self)
        self.button2.setGeometry(200, 150, 100, 50)
        self.button2.setStyleSheet("border: 2px solid black; background-image : url(Img/iesiti.png);")
        self.button2.move(150,520)
        self.button2.clicked.connect(self.closed)


    def closed(self):


        sys.exit()

    def clicked_Scriere(self):
        self.cams = Scriere()
        self.cams.show()
        self.close()

    def clicked_Vorbire(self):
        self.cams = Vorbire()
        self.cams.show()
        self.close()



class Scriere(QMainWindow):

    def  __init__(self):
        super(Scriere, self).__init__()
        self.initUI()
        self.setFixedSize(400, 600)
        x, y = centrare()
        self.setGeometry(x, y,400,600)
        self.setWindowTitle("Scriere")
        oImage = QImage("Img/chatbox.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)



    def initUI(self):


        self.imagine_user = QLabel(self)
        self.pixmap = QPixmap('Img/user1.png')


        self.imagine_bot = QLabel(self)
        self.pixmap2 = QPixmap('Img/bot.png')



        self.label1 = QLabel(self)
        self.label1.setText("")
        self.label1.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label1.setFont(QFont('', 15))

        self.label1.adjustSize()
        latime = self.label1.width()
        inaltime = self.label1.height()


        self.label1.move(20,100)


        self.label2 = QtWidgets.QLabel(self)
        self.label2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label2.setText("")





        self.textbox = QLineEdit(self)
        self.textbox.returnPressed.connect(self.on_click)
        self.textbox.move(20, 560)
        self.textbox.resize(300, 30)

        # Create a button in the window

        self.trimite = QPushButton('', self)
        self.trimite.setGeometry(200, 150, 50, 30)
        self.trimite.setStyleSheet("border-radius : 5 ;border: 1px solid black; background-image : url(Img/sent.png);")
        self.trimite.move(330, 560)
        self.trimite.clicked.connect(self.on_click)

        self.iesi = QPushButton('', self)
        self.iesi.setGeometry(200, 150, 50, 50)
        self.iesi.setStyleSheet("border-radius : 25 ;border: 0.1px solid black; background-image : url(Img/close.png);")
        self.iesi.move(330, 10)
        self.iesi.clicked.connect(self.closed)

        self.inapoi = QPushButton('', self)
        self.inapoi.setGeometry(200, 150, 50, 50)
        self.inapoi.setStyleSheet("border-radius : 25 ;border: 0.1px solid black; background-image : url(Img/back.png);")
        self.inapoi.move(260, 10)
        self.inapoi.clicked.connect(self.clicked_back)






    def update_label1(self):
        self.imagine_user.setPixmap(self.pixmap)
        self.imagine_user.resize(20,20)
        self.imagine_user.move(10, 102)

        self.label1.setStyleSheet("QLabel{margin-left: 20px; border: 0.1px solid black; border-radius: 10px; background: #0099ff; color: white;}");
        inaltime = self.label1.height()
        self.label1.adjustSize()
        latime = self.label1.width()
        latime_2 = self.label2.width()


        if latime > 250:
            self.label1.setMinimumWidth(250)
            self.label1.setWordWrap(True)
            self.label1.adjustSize()
            self.label1.setMinimumWidth(0)

        self.label1.adjustSize()




        self.label2.move(380 - latime_2, 130 + inaltime)

        self.imagine_bot.setPixmap(self.pixmap2)
        self.imagine_bot.resize(20,20)
        self.imagine_bot.move(370 - latime_2, 132 + inaltime)

        x = self.label1.width() + 5
        y = self.label1.height() + 5
        self.label1.resize(x, y)



    def update_label2(self):

        self.label2.setWordWrap(False)
        self.label2.setFont(QFont('Arial', 15))
        self.label2.adjustSize()

        latime_label2 = self.label2.width()


        if  latime_label2 > 250:
            self.label2.setMinimumWidth(250)
            self.label2.setWordWrap(True)
            self.label2.adjustSize()
            self.label2.setMinimumWidth(0)


        x = self.label2.width() + 5
        y = self.label2.height() + 5
        self.label2.resize(x, y)
        self.label2.setStyleSheet("QLabel{margin-left: 20px; border: 0.1px solid black; border-radius: 10px; background: green; color: white;}");



    def on_click(self):


        inp = self.textbox.text()
        rezultat = model.predict([bag_of_words(inp, words)])[0]
        rezultat_index = numpy.argmax(rezultat)
        tag = labels[rezultat_index]

        if rezultat[rezultat_index] > 0.7:

            for tg in data["intents"]:
                if tg['tag'] == tag:

                    raspuns = tg['responses']
                    raspuns_final = random.choice(raspuns)
        else:
            raspuns_final = "Nu știu încă răspunsul.Încearcă altă întrebare!"



        raspuns_printat = diacritice(raspuns_final)

        if len(inp) == 0:
            self.label1.hide()
            self.imagine_user.hide()
            self.imagine_bot.setPixmap(self.pixmap2)
            self.imagine_bot.resize(20, 20)
            self.imagine_bot.move(194, 132)
            self.label2.move(198, 132 )
            self.label2.setText("Nu ati scris nimic!")
            self.label2.setFont(QFont('Arial', 15))
            self.label2.setStyleSheet("QLabel{margin-left: 20px; border: 0.1px solid black; border-radius: 10px; background: green; color: white;}");
            self.label2.adjustSize()
            self.textbox.setText("")

        else:

            self.imagine_user.show()
            self.label1.show()
            self.label1.setText(inp)
            self.update_label1()
            self.update_label2()
            self.label2.setText(raspuns_printat)
            self.update_label2()
            self.update_label1()
            self.textbox.setText("")
            playsound("Sounds/message_sound.mp3")
            QApplication.processEvents()


    def closed(self):


        sys.exit()



    def clicked_back(self):
        self.cams = MainWindow()
        self.cams.show()
        self.close()

class Vorbire(QMainWindow):

    def  __init__(self):
        super(Vorbire, self).__init__()
        self.initUI()
        self.setFixedSize(400, 600)
        x, y = centrare()
        self.setGeometry(x, y,400,600)
        self.setWindowTitle("Vorbire")
        oImage = QImage("Img/chatbox.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)


    def initUI(self):


        self.imagine_user = QLabel(self)
        self.pixmap = QPixmap('Img/user1.png')


        self.imagine_bot = QLabel(self)
        self.pixmap2 = QPixmap('Img/bot.png')

        self.ascult = QLabel(self)
        self.ascult.setText("")
        self.ascult.setFont(QFont('Arial', 15))
        self.ascult.move(150,480)


        self.label1 = QLabel(self)
        self.label1.setText("")
        self.label1.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label1.setFont(QFont('Arial', 15))

        self.label1.adjustSize()



        self.label1.move(20,100)


        self.label2 = QtWidgets.QLabel(self)
        self.label2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label2.setText("")


        self.vorbiti = QPushButton('', self)
        self.vorbiti.setGeometry(200, 150, 80, 80)
        self.vorbiti.setStyleSheet("border-radius : 40 ;border: 0.1px solid black; background-image : url(Img/vorbiti.png);")
        self.vorbiti.move(160, 510)
        self.vorbiti.clicked.connect(self.clicked)

        self.iesi = QPushButton('', self)
        self.iesi.setGeometry(200, 150, 50, 50)
        self.iesi.setStyleSheet("border-radius : 25 ;border: 0.1px solid black; background-image : url(Img/close.png);")
        self.iesi.move(330, 10)
        self.iesi.clicked.connect(self.closed)

        self.inapoi = QPushButton('', self)
        self.inapoi.setGeometry(200, 150, 50, 50)
        self.inapoi.setStyleSheet("border-radius : 25 ;border: 0.1px solid black; background-image : url(Img/back.png);")
        self.inapoi.move(260, 10)
        self.inapoi.clicked.connect(self.clicked_back)



    @QtCore.pyqtSlot()



    def clicked(self):

        self.vorbiti.hide()
        self.iesi.setEnabled(False)
        self.inapoi.setEnabled(False)
        self.update_ascult()
        playsound("Sounds/start_record.mp3")
        QApplication.processEvents()

        r = sr.Recognizer()
        m = sr.Microphone()

        inp = ""
        with m as source:
            audio = r.listen(source, timeout=1, phrase_time_limit=5)
            playsound("Sounds/stop_record.mp3")
            self.ascult.hide()
            QApplication.processEvents()

            try:
                inp = r.recognize_google(audio, language=limba)

                self.ascult.setText("")
                self.ascult.hide()
                inp_printat = str(inp)
                self.label1.setText(inp_printat)
                self.update_label1()
                self.update_label2()
                self.label2.hide()
                QApplication.processEvents()



            except sr.UnknownValueError:

                self.label2.setText("Nu am inteles ce ati spus, incercati din nou")
                self.update_label2()
                self.label2.move(100, 132 )
                QApplication.processEvents()
                playsound("error.mp3")
                time.sleep(2.5)


            finally:
                pass



        if len(inp) == 0:

            self.cams = Vorbire()
            self.cams.show()
            self.close()

        else:

            rezultat = model.predict([bag_of_words(inp, words)])[0]
            rezultat_index = numpy.argmax(rezultat)
            tag = labels[rezultat_index]

            if rezultat[rezultat_index] > 0.7:

                for tg in data["intents"]:
                    if tg['tag'] == tag:
                        raspuns = tg['responses']
                        raspuns_final = random.choice(raspuns)

            else:
                raspuns_final = "Nu știu încă răspunsul.Încearcă altă întrebare!"

            raspuns_printat = diacritice(raspuns_final)
            self.output = gTTS(text=raspuns_printat, lang=limba, slow=False)

            name = "output2.mp3"
            self.output.save(name)

            self.label2.setText(raspuns_printat)
            self.imagine_bot.show()
            self.update_label2()
            self.update_label1()
            QApplication.processEvents()

            playsound(name)
            os.remove(name)
            self.vorbiti.show()
            QApplication.processEvents()
            self.butoane()



    def butoane(self):
        self.iesi.setEnabled(True)
        self.inapoi.setEnabled(True)

    def closed(self):

        sys.exit()

    def update_ascult(self):

        self.ascult.setStyleSheet("QLabel{margin-left: 20px; border: 0.1px solid black; border-radius: 10px; background: grey; color: white;}");
        self.ascult.setText("Ascult")
        self.ascult.adjustSize()
        self.label1.hide()
        self.label2.hide()
        self.imagine_bot.hide()
        self.imagine_user.hide()
        self.ascult.show()


    def update_label1(self):
            self.imagine_user.setPixmap(self.pixmap)
            self.imagine_user.resize(20,20)
            self.imagine_user.move(10, 102)
            self.label1.setStyleSheet("QLabel{margin-left: 20px; border: 0.1px solid black; border-radius: 10px; background: #0099ff; color: white;}");
            inaltime = self.label1.height()
            self.label1.adjustSize()
            latime = self.label1.width()
            latime_2 = self.label2.width()


            if latime > 250:
                self.label1.setMinimumWidth(250)
                self.label1.setWordWrap(True)
                self.label1.adjustSize()
                self.label1.setMinimumWidth(0)

            self.label1.adjustSize()




            self.label2.move(380 - latime_2, 130 + inaltime)

            self.imagine_bot.setPixmap(self.pixmap2)
            self.imagine_bot.resize(20,20)
            self.imagine_bot.move(370 - latime_2, 132 + inaltime)

            x = self.label1.width() + 5
            y = self.label1.height() + 5
            self.label1.resize(x, y)

            self.imagine_user.show()
            self.label1.show()




    def update_label2(self):

        self.label2.setWordWrap(False)
        self.label2.setFont(QFont('Arial', 15))
        self.label2.adjustSize()

        latime_label2 = self.label2.width()


        if  latime_label2 > 250:
            self.label2.setMinimumWidth(250)
            self.label2.setWordWrap(True)
            self.label2.adjustSize()
            self.label2.setMinimumWidth(0)


        x = self.label2.width() + 5
        y = self.label2.height() + 5
        self.label2.resize(x, y)
        self.label2.setStyleSheet("QLabel{margin-left: 20px; border: 0.1px solid black; border-radius: 10px; background: green; color: white;}");
        self.label2.show()



    def clicked_back(self):
        self.cams = MainWindow()
        self.cams.show()
        self.close()



def window():
    app = QApplication(sys.argv)
    win = MainWindow()


    win.show()
    sys.exit(app.exec_())

window()
