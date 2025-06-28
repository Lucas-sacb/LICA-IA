# -*- coding: utf-8 -*-
# Código original por Lucas sacb @lucas_sacb
# Corrigido e atualizado por "Python" (IA Assistente)

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class WhatsAppBot:
    """
    Uma classe para automatizar respostas no WhatsApp Web, respondendo a conversas
    não lidas e não silenciadas.
    """
    def __init__(self):
        # --- Configuração do ChatterBot ---
        print("INFO: Configurando a IA (ChatterBot)...")
        self.chatbot = ChatBot('Lica')
        # Descomente as linhas abaixo apenas na primeira execução para treinar o bot.
        # Após o primeiro treino, o banco de dados 'db.sqlite3' é criado e não é mais necessário treinar.
        # if not os.path.exists('db.sqlite3'):
        #     print("INFO: Treinando o bot pela primeira vez. Isso pode levar alguns minutos...")
        #     trainer = ChatterBotCorpusTrainer(self.chatbot)
        #     trainer.train('chatterbot.corpus.portuguese')
        #     print("INFO: Treinamento concluído.")
        # else:
        #     print("INFO: Banco de dados de treinamento já existe. Pulando treinamento.")
            
        # --- Configuração do Selenium ---
        print("INFO: Iniciando o navegador Chrome...")
        # Usamos webdriver-manager para instalar e gerenciar o chromedriver automaticamente
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, 20) # Define um tempo de espera explícito

        # --- Abrir WhatsApp Web ---
        print("INFO: Abrindo o WhatsApp Web. Por favor, escaneie o QR Code.")
        self.driver.get("https://web.whatsapp.com/")
        # Espera até que a lista de conversas apareça, indicando que o login foi feito
        self.wait.until(
            EC.presence_of_element_located((By.ID, "side"))
        )
        print("INFO: Login realizado com sucesso!")

    def encontrar_conversas_nao_lidas(self):
        """
        Encontra e retorna a primeira conversa com mensagem não lida
        que não esteja silenciada.
        """
        try:
            # O seletor para o ponto de notificação de nova mensagem é um span com a classe 'x6s0dn4'
            # e para o ícone de silenciado é 'data-testid="icon-muted"'
            painel_conversas = self.driver.find_element(By.ID, "pane-side")
            
            # Busca por todas as conversas que possuem notificação de não lida
            conversas_nao_lidas = painel_conversas.find_elements(By.CSS_SELECTOR, "div.x6s0dn4.x78zum5.x1q0g3np.x1iyjqo2.x1qughib")
            
            for conversa in conversas_nao_lidas:
                try:
                    # Dentro do elemento da conversa, verifica se existe o ícone de silenciado
                    conversa.find_element(By.CSS_SELECTOR, 'span[data-testid="icon-muted"]')
                    # Se encontrou, a conversa está silenciada, então pulamos para a próxima
                    print("DEBUG: Conversa com nova mensagem encontrada, mas está silenciada. Ignorando.")
                    continue
                except NoSuchElementException:
                    # Se não encontrou o ícone, a conversa não está silenciada!
                    print("INFO: Conversa não lida e não silenciada encontrada!")
                    return conversa

        except NoSuchElementException:
            # Nenhum ponto verde de notificação foi encontrado
            return None
        except Exception as e:
            print(f"ERRO: Erro inesperado ao procurar conversas: {e}")
            return None
        
        return None

    def ler_ultima_mensagem(self):
        """
        Lê a última mensagem da conversa atualmente aberta.
        """
        try:
            # O seletor para as mensagens pode variar. Este é um dos mais comuns.
            # `div.copyable-text` geralmente contém o texto da mensagem.
            elementos_msg = self.driver.find_elements(By.CSS_SELECTOR, "div.copyable-text")
            
            if elementos_msg:
                # A última mensagem é o último elemento da lista
                ultima_msg_texto = elementos_msg[-1].text
                print(f"DEBUG: Última mensagem lida: '{ultima_msg_texto}'")
                return ultima_msg_texto
            return None
        except Exception as e:
            print(f"ERRO: Não foi possível ler a última mensagem: {e}")
            return None

    def enviar_mensagem(self, resposta):
        """
        Digita e envia uma mensagem para a conversa aberta.
        """
        try:
            # Seletor da caixa de texto, usando 'data-testid' que é mais estável
            caixa_de_texto = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="conversation-compose-box-input"]'))
            )
            caixa_de_texto.click()
            time.sleep(1) # Pequena pausa para garantir que o cursor está ativo
            caixa_de_texto.send_keys(resposta)
            time.sleep(1) # Pausa para a mensagem ser digitada
            caixa_de_texto.send_keys(Keys.ENTER)
            print(f"INFO: Resposta enviada: '{resposta}'")
            return True
        except TimeoutException:
            print("ERRO: A caixa de texto não foi encontrada a tempo.")
            return False
        except Exception as e:
            print(f"ERRO: Falha ao enviar a mensagem: {e}")
            return False

    def iniciar(self):
        """
        Inicia o loop principal do bot.
        """
        ultima_mensagem_processada = ""
        while True:
            try:
                print("\nINFO: Procurando por novas mensagens...")
                conversa_alvo = self.encontrar_conversas_nao_lidas()

                if conversa_alvo:
                    # Clica na conversa para abri-la
                    conversa_alvo.click()
                    time.sleep(2) # Aguarda a conversa carregar

                    # Lê a última mensagem
                    nova_mensagem = self.ler_ultima_mensagem()

                    # Verifica se a mensagem é nova e não foi processada anteriormente
                    if nova_mensagem and nova_mensagem != ultima_mensagem_processada:
                        ultima_mensagem_processada = nova_mensagem
                        
                        # Gera uma resposta com o ChatterBot
                        print("INFO: Gerando resposta com a IA...")
                        resposta_bot = self.chatbot.get_response(nova_mensagem)
                        
                        # Envia a resposta
                        self.enviar_mensagem(str(resposta_bot))
                        
                        # Espera um pouco antes de procurar a próxima para não sobrecarregar
                        time.sleep(5)
                    else:
                        print("DEBUG: Mensagem repetida ou vazia. Ignorando.")

                # Pausa antes de verificar novamente para não usar muito CPU
                time.sleep(10)

            except Exception as e:
                print(f"ERRO: Ocorreu um erro no loop principal: {e}")
                # Em caso de erro grave, espera um pouco mais antes de tentar novamente
                time.sleep(60)

if __name__ == "__main__":
    bot = WhatsAppBot()
    bot.iniciar()
