import psycopg2
from datetime import datetime 
import getpass
from time import sleep


def ping():
    """Vai pingar IP definido no Prompt do Windows.

    Returns:
        int: ping.
    """    
    import os
    comando = os.popen(f'ping {endereco} | FIND "Média =" ')
    resultado = comando.read()
    inicio = resultado.find('M‚dia =') + len('M,dia =')
    return resultado[inicio:].replace('ms','').strip()


#entradas
endereco = input('IP: ')
hostname = input('Hostname: ')
bd = input('Banco de dados: ')
usuario = input('Usuário: ')
senha = getpass.getpass(prompt='Senha [Por motivos de segurança os caracteres serão ocultados]: ', stream=None)
tempo = int(input('Em qual intervalo, em MINUTOS, você gostaria de pingar o endereço IP? '))

#loop de tempo
while True:

    #conexão com o banco de dados Postgrees
    while True:
        try:
            con = psycopg2.connect(host=f'{hostname}', database=f'{bd}', user=f'{usuario}', password=f'{senha}')
            break
        except psycopg2.OperationalError:
            print('ERRO! NÃO FOI POSSÍVEL CONECTAR AO BANCO DE DADOS. INSIRA OS DADOS NOVAMENTE: ')
            endereco = input('IP: ')
            hostname = input('Hostname: ')
            bd = input('Banco de dados: ')
            usuario = input('Usuário: ')
            senha = getpass.getpass(prompt='Senha [Por motivos de segurança os caracteres serão ocultados]: ', stream=None)

    #cursor
    cur = con.cursor()

    #comando SQL e execução
    sql = 'CREATE TABLE IF NOT EXISTS pings (id BIGSERIAL PRIMARY KEY, dia DATE NOT NULL, horario TIME NOT NULL, ping INT NOT NULL);'
    cur.execute(sql)
    sql = f"insert into pings values (default, '{datetime.now().strftime('%Y-%m-%d')}', '{datetime.now().strftime('%H:%M:%S')}', '{ping()}')"
    cur.execute(sql)
    print(f"DADOS INSERIDOS NA TABELA 'pings' AS {datetime.now().strftime('%H:%M')} h COM SUCESSO!")

    #salvando e fechando
    con.commit()
    con.close()

    #aguardando o tempo definido
    sleep(tempo*60)
