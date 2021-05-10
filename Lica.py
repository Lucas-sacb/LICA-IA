# -*- coding: utf-8 -*-
#By Lucas sacb @lucas_sacb

from selenium import webdriver
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import time
from selenium import webdriver
import os
from time import sleep
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


#Create um noco chatbot como o nome de Lica
chatbot = ChatBot('Lica')
# cria um novo trainer para o chatbot
trainer = ChatterBotCorpusTrainer(chatbot)
#Usa uma arquivo pré existente para buscar respostas
trainer.train('chatterbot.corpus.portuguese')

class zapbot:

    def __init__(self):
        # Inicializa o webdriver
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # Abre o whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        # Aguarda alguns segundos para validação manual do QrCode
        self.driver.implicitly_wait(20)
        sleep(30)

    def ultima_msg(self):
        """ Captura a ultima mensagem da conversa """
        try:
            post = self.driver.find_elements_by_class_name("_1dB-m")
            ultimo = len(post) - 1
            # O texto da ultima mensagem
            texto = post[ultimo].find_element_by_css_selector(
                "span.selectable-text").text
            return texto
        except Exception as e:
            print("Erro ao ler msg, tentando novamente!")

    def envia_msg(self, msg):
        """ Envia uma mensagem para a conversa aberta """
        # Seleciona acaixa de mensagem
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("DuUXI")
        sleep(3)
        # Digita a mensagem
        self.caixa_de_mensagem.send_keys(msg)
        sleep(5)
        # botão enviar
        self.caixa_de_mensagem.send_keys(Keys.ENTER)
        sleep(4)
        #self.caixa_de_mensagem.send_keys(Keys.ENTER)
        sleep(4)

    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        sleep(15)
        # Seleciona a caixa de pesquisa de conversa
        self.caixa_de_pesquisa = self.driver.find_element_by_class_name("_1awRl")
        # Digita o nome ou numero do contato
        self.caixa_de_pesquisa.send_keys(contato)
        sleep(10)
        # Seleciona o contato
        self.contato = self.driver.find_element_by_xpath("//span[@title = '{}']".format(contato))
        # Entra na conversa
        self.contato.click()


bot = zapbot()
bot.abre_conversa( "Gruo Test" )
bot.envia_msg( "Lica: Ola, eu sou a lica." )
bot.envia_msg( "Lica: Para conversarmos digite: /conversar" )
msg = ""
while msg != "/quit":
    sleep(1)
    msg = bot.ultima_msg()
    if msg == "//":
        bot.envia_msg( "Lica: Esse é um texto com os comandos válidos:" )
        bot.envia_msg( "/conversar (para iniciarmos um dialogo, digite /q para encerrar)" )
        bot.envia_msg( "/quit (para sair)" ) 
    elif msg == "/conversar":
      msg =="/quit"
      sleep(5)
      bot.envia_msg( "Lica: Ola, como vai vc?" )
      sleep(5)
      request=""
      while request != "/q":
        request = bot.ultima_msg()
        sleep(5)
        response = str(chatbot.get_response(request))
        sleep(10)
        bot.envia_msg(response)
        sleep(2)
    elif msg == "/quit":
        bot.envia_msg("Bye bye!")
