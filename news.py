import requests
from bs4 import BeautifulSoup
import webbrowser
import os
from colorama import init, Fore, Style

# Inicializa o colorama
init(autoreset=True)

class Site:
    def __init__(self, site):
        self.site = site
        self.news = []
        self.noticias_por_pagina = 10  # 10 noticias por pagina

    def update_news(self):
        if self.site.lower() == 'globo':
            url = 'https://globo.com/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}

            page = requests.get(url, headers=headers)

            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')

            noticias = soup.find_all('a')

            tg_class1 = 'post__title'
            tg_class2 = 'post-multicontent__link--title__text'

            for noticia in noticias:
                if noticia.h2 is not None:
                    if tg_class1 in noticia.h2.get('class') or tg_class2 in noticia.h2.get('class'):
                        news_dict_globo = {'noticia': noticia.h2.text, 'link': noticia.get('href')}
                        self.news.append(news_dict_globo)

    def view(self):
        pagina_inicial = 0
        while True:
            inicio = pagina_inicial * self.noticias_por_pagina
            final = inicio + self.noticias_por_pagina
            mostrar_noticias = self.news[inicio:final]
            os.system('cls' if os.name == 'nt' else 'clear')
            self.boas_vindas()  # Exibe a mensagem de boas-vindas a cada limpeza de tela
            print(f'\n{Fore.CYAN}Pagina {pagina_inicial + 1}{Style.RESET_ALL}')

            for i, item in enumerate(mostrar_noticias, inicio):
                print(f"{Fore.YELLOW}[{i}] - {item['noticia']}{Style.RESET_ALL}")

            # Opções de navegação
            print("\nOpções:")
            print(f"{Fore.GREEN}Digite o número da notícia para abrir.{Style.RESET_ALL}")

            if pagina_inicial > 0:
                print(f"{Fore.BLUE}[P] Página anterior{Style.RESET_ALL}")
            if final < len(self.news):
                print(f"{Fore.BLUE}[N] Próxima página{Style.RESET_ALL}")
            print(f"{Fore.RED}[S] Sair{Style.RESET_ALL}")

            escolha = input('>>').lower().strip()

            if escolha.isdigit():
                link_escolhido = self.news[int(escolha)]['link']
                webbrowser.open(link_escolhido)
            elif escolha == 'p':
                if pagina_inicial == 0:
                    pass
                else:
                    pagina_inicial -= 1
            elif escolha == 'n':
                pagina_inicial += 1
            elif escolha == 's':
                print(f'{Fore.GREEN}Programa encerrado com sucesso...{Style.RESET_ALL}')
                break
            else:
                print(f'{Fore.RED}Informou uma opção inválida...{Style.RESET_ALL}')

    @staticmethod
    def boas_vindas():
        print(Fore.MAGENTA + r"""
   _____ _       _                               
  / ____| |     | |                              
 | |  __| | ___ | |__   ___   ___ ___  _ __ ___  
 | | |_ | |/ _ \| '_ \ / _ \ / __/ _ \| '_ ` _ \ 
 | |__| | | (_) | |_) | (_) | (_| (_) | | | | | |
  \_____|_|\___/|_.__/ \___(_)___\___/|_| |_| |_|
                                                 
                                                 
    """)
        print(Fore.CYAN + "Bem-vindo ao agregador de notícias!")
        print("Desenvolvido por TonDevPy\n" + Style.RESET_ALL)

# Executa a função de boas-vindas antes de começar
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    globo = Site('globo')
    globo.update_news()
    globo.view()
