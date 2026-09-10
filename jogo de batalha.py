"""
Cada Personagem vai ter: energia , ataque , vida , especial , nome , defesa ;

Vão ser 5 personagens: Cavaleiro , Mago , Arqueiro , Ogro , Dragão;
                           2         3        1        4       6
Vão ser 2 Jogadores: Cada um começará com 10 fichas, que serão usadas para comprar os personagens acima ;

Ganha quem derrotar todos os personagens do outro jogador ;

O especial de cada personagem será recarregado (+5 de energia) conforme o passar dos turnos ;

Em cada turno o jogador deve decidir qual personagem ele quer atacar e qual personagem ele usará
(mas, dependendo do especial, o ataque pode ser múltiplo) ;

Cada personagem terá uma defesa padrão automática;
"""

import os
import subprocess
from tabulate import tabulate


class Personagem:
    def __init__(self, vida, energia, defesa, nome_ataque, ataque, nome):
        self.nome_ataque = nome_ataque
        self.energia = energia          # essa energia começa em 0
        self.ataque = ataque
        self.vida = vida
        self.nome = nome
        self.defesa = defesa

    def atacando(self, ataque, outro_personagem):
        # usa max(0, ...) para o ataque nunca "curar" o alvo
        # quando a defesa é maior que o ataque
        dano_causado = max(0, ataque - outro_personagem.defesa)
        outro_personagem.vida -= dano_causado
        return dano_causado

    def esta_vivo(self):
        return self.vida > 0

    def recarregar_energia(self, quantidade=5):
        # implementa a regra "+5 de energia conforme o passar dos turnos"
        if self.esta_vivo():
            self.energia += quantidade


class Especial(Personagem):
    def __init__(self, vida, energia, defesa, nome_ataque, ataque, nome,
                 nome_especial, ataque_especial, energia_especial, alvos_especial):
        super().__init__(vida, energia, defesa, nome_ataque, ataque, nome)
        self.nome_especial = nome_especial
        self.ataque_especial = ataque_especial
        self.energia_especial = energia_especial
        self.alvos_especial = alvos_especial

    def pode_usar_especial(self):
        return self.energia >= self.energia_especial

    def usando_especial(self, lista_alvos):
        if not self.pode_usar_especial():
            print("O personagem não possui energia suficiente!")
            return []

        resultados = []
        for alvo in lista_alvos[:self.alvos_especial]:
            dano_causado = max(0, self.ataque_especial - alvo.defesa)
            alvo.vida -= dano_causado
            resultados.append((alvo.nome, dano_causado))

        self.energia = 0
        return resultados


class Mago(Especial):
    def __init__(self, nome):
        super().__init__(30, 0, 3, "bola de fogo", 10, nome, "chuva de meteoritos", 8, 20, 3)


class Ogro(Especial):
    def __init__(self, nome):
        super().__init__(50, 0, 5, "soco atordoador", 10, nome, "faz o urro", 10, 25, 3)


class Dragao(Especial):
    def __init__(self, nome):
        super().__init__(70, 0, 2, "cauda chicote", 12, nome, "cuspe elétrico", 15, 30, 3)


class Arqueiro(Especial):
    def __init__(self, nome):
        super().__init__(20, 0, 3, "flecha precisa", 8, nome, "ataque explosivo", 15, 15, 2)


class Cavaleiro(Especial):
    def __init__(self, nome):
        super().__init__(40, 0, 5, "esgrima tradicional", 8, nome, "espada mágica", 30, 25, 1)


# ---------- Funções auxiliares ----------

def limpar_tela():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)


def ler_inteiro(mensagem):
    # evita que o programa quebre se o jogador digitar algo que não é número
    while True:
        entrada = input(mensagem).strip()
        if entrada.isdigit():
            return int(entrada)
        print("Entrada inválida! Digite um número.")


def time_vivo(time):
    return [p for p in time if p.esta_vivo()]


def mostrar_time(time, titulo):
    linhas = []
    for p in time:
        status = "Vivo" if p.esta_vivo() else "Derrotado"
        especial_pronto = "Sim" if isinstance(p, Especial) and p.pode_usar_especial() else "Não"
        linhas.append([p.nome, p.vida, p.energia, p.defesa, especial_pronto, status])
    print(f"\n--- {titulo} ---")
    print(tabulate(linhas, headers=["Nome", "Vida", "Energia", "Defesa", "Especial pronto?", "Status"],
                    tablefmt="grid"))


def escolher_personagem(time, mensagem):
    vivos = time_vivo(time)
    for idx, p in enumerate(vivos, start=1):
        print(f"{idx}. {p.nome} (Vida: {p.vida}, Energia: {p.energia})")
    while True:
        escolha = ler_inteiro(mensagem)
        if 1 <= escolha <= len(vivos):
            return vivos[escolha - 1]
        print("Escolha inválida!")


def escolher_alvos(time_inimigo, quantidade):
    vivos = time_vivo(time_inimigo)
    quantidade = min(quantidade, len(vivos))
    disponiveis = vivos.copy()
    alvos = []
    for i in range(quantidade):
        print(f"\nEscolha o alvo {i + 1} de {quantidade}:")
        for idx, p in enumerate(disponiveis, start=1):
            print(f"{idx}. {p.nome} (Vida: {p.vida})")
        while True:
            escolha = ler_inteiro("Insira o número do alvo: ")
            if 1 <= escolha <= len(disponiveis):
                alvos.append(disponiveis.pop(escolha - 1))
                break
            print("Escolha inválida!")
    return alvos


def jogar_turno(numero_jogador, time_atual, time_inimigo):
    limpar_tela()
    print(f"=== Turno do Jogador {numero_jogador} ===")
    mostrar_time(time_atual, f"Seu time (Jogador {numero_jogador})")
    mostrar_time(time_inimigo, "Time inimigo")

    print("\nEscolha o personagem que irá agir:")
    atacante = escolher_personagem(time_atual, "Insira o número do personagem: ")

    pode_especial = isinstance(atacante, Especial) and atacante.pode_usar_especial()
    print(f"\n{atacante.nome} está pronto para agir!")
    print(f"1. Ataque normal ({atacante.nome_ataque})")
    if pode_especial:
        print(f"2. Especial: {atacante.nome_especial}")
    else:
        print("2. Especial (indisponível - energia insuficiente)")

    while True:
        opcao = ler_inteiro("Escolha a ação: ")
        if opcao == 1:
            alvo = escolher_alvos(time_inimigo, 1)[0]
            dano = atacante.atacando(atacante.ataque, alvo)
            print(f"\n{atacante.nome} atacou {alvo.nome} com {atacante.nome_ataque}, causando {dano} de dano!")
            break
        elif opcao == 2 and pode_especial:
            alvos = escolher_alvos(time_inimigo, atacante.alvos_especial)
            resultados = atacante.usando_especial(alvos)
            print(f"\n{atacante.nome} usou {atacante.nome_especial}!")
            for nome, dano in resultados:
                print(f" - {nome} sofreu {dano} de dano")
            break
        else:
            print("Opção inválida!")

    # Regra do jogo: energia especial recarrega (+5) conforme o passar dos turnos
    for p in time_vivo(time_atual) + time_vivo(time_inimigo):
        p.recarregar_energia(5)

    input("\nPressione Enter para continuar...")


# ---------- Programa principal ----------

def main():
    print("Bem - vindos ao jogo ****** Batalha Mágica ******\n\n"
          "O jogo será em turnos então, antes de começar, tirem sortes para ver quem será "
          "o Jogador 1 (que começará primeiro) e quem será o Jogador 2")
    input("\nPressione Enter para continuar...")

    limpar_tela()

    print("Já decididos os jogadores vamos definir o exército de cada um! \n"
          "Vocês dois começarão inicialmente com 10 fichas e as usarão para adquirir suas tropas")
    cabecalho = ["Atributo", "Mago (1)", "Ogro (2)", "Dragão (3)", "Arqueiro (4)", "Cavaleiro (5)"]
    tabela = [
        ["Ataque Padrão", 10, 10, 12, 8, 8],
        ["Ataque Especial", 8, 10, 15, 15, 30],
        ["Alvos do Especial", 3, 3, 3, 2, 1],
        ["Defesa", 3, 5, 2, 3, 5],
        ["Energia do Especial", 20, 25, 30, 15, 25],
        ["Fichas Necessárias", 3, 4, 6, 1, 2],
    ]

    custos = {1: (3, "Mago"), 2: (4, "Ogro"), 3: (6, "Dragão"), 4: (1, "Arqueiro"), 5: (2, "Cavaleiro")}
    classes = {1: Mago, 2: Ogro, 3: Dragao, 4: Arqueiro, 5: Cavaleiro}

    jogador1 = []
    jogador2 = []

    for i in range(2):
        lista_temporaria = []
        # contadores resetados a cada jogador, então cada um começa
        # sua numeração do zero (Mago 1, Mago 2...) em vez de continuar do outro jogador
        contadores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        print(f"\nAgora é a vez do Jogador {i + 1} escolher! Você possui 10 fichas. "
              "Para escolher o personagem, insira o número (que está em parênteses) correspondente ao personagem")
        print("Aqui estão os personagens, as características e os valores de cada um:\n")
        print(tabulate(tabela, headers=cabecalho, tablefmt="grid"))

        fichas = 10
        while fichas > 0:
            print(f"\nFichas restantes: {fichas}")
            p = ler_inteiro("Insira um número (1 a 5): ")

            if p not in custos:
                print("Número inválido! Digite entre 1 e 5.")
                continue

            custo, nome_tipo = custos[p]
            if fichas < custo:
                print(f"Você não tem fichas suficientes para o {nome_tipo}!")
                continue

            contadores[p] += 1
            nome = f"{nome_tipo} {contadores[p]} (J{i + 1})"
            objeto = classes[p](nome)
            lista_temporaria.append(objeto)
            fichas -= custo
            print(f"+1 {nome_tipo} ({nome})")

        input("\nPressione Enter para continuar...")

        if i == 0:
            jogador1 = lista_temporaria.copy()
        else:
            jogador2 = lista_temporaria.copy()

        limpar_tela()

    # menu interativo de batalha
    print("Exércitos formados! A batalha vai começar!")
    input("Pressione Enter para continuar...")

    times = [jogador1, jogador2]
    turno = 0

    while True:
        atual = turno % 2
        inimigo = 1 - atual

        jogar_turno(atual + 1, times[atual], times[inimigo])

        if not time_vivo(times[inimigo]):
            limpar_tela()
            print(f"🏆 O Jogador {atual + 1} venceu a batalha! 🏆")
            break

        turno += 1


if __name__ == "__main__":
    main()