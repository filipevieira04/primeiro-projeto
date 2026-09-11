Este repositório contém um jogo de batalha medieval por turnos feito para dois jogadores

Este jogo feito na linguagem python

## Como rodar o projeto

1. Instale o [Python](https://www.python.org/downloads/) 3.8 ou superior.
2. Abra o terminal na pasta do projeto.
3. Instale a dependência do jogo:

```bash
python -m pip install tabulate
```

4. Execute o jogo:

No Windows:

```bash
python "jogo de batalha.py"
```

No Linux ou macOS, se necessário, use `python3`:

```bash
python3 "jogo de batalha.py"
```

O jogo é interativo e deve ser jogado por dois jogadores no mesmo terminal.

* REGRAS DO JOGO:

Cada Personagem vai ter: energia , ataque , vida , especial , nome , defesa ;

Vão ser 5 personagens: Cavaleiro , Mago , Arqueiro , Ogro , Dragão;
                           
Vão ser 2 Jogadores: Cada um começará com 10 fichas, que serão usadas para comprar os personagens acima ;

Ganha quem derrotar todos os personagens do outro jogador ;

O especial de cada personagem será recarregado (+5 de energia) conforme o passar dos turnos ;

Em cada turno o jogador deve decidir qual personagem ele quer atacar e qual personagem ele usará
(mas, dependendo do especial, o ataque pode ser múltiplo) ;

Cada personagem terá uma defesa padrão automática;
