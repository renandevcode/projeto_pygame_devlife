# Checks de estudo de Pygame

Este é um projeto desenvolvido na disciplina Developer Life, do 1o semestre do curso de Ciência da Computação do Insper. O intuito deste projeto é aprender e praticar o uso da biblioteca Pygame para o desenvolvimento de jogos 2D usando Python.

## Descrição do jogo

Jogo de nave em que o jogador deve desviar dos meteoros e atirar para destruí-los. A nave começa com três vidas, representadas por corações no canto superior esquerdo. Cada colisão com um meteoro tira uma vida. Ao perder todas as vidas, aparece a tela de game over, com a opção de começar uma nova partida.

O jogo possui fundo estrelado, indicador de FPS, música de fundo, som de tiro e animação de explosão dos meteoros. O código está organizado em classes para o jogo, as telas e os sprites.

## Como jogar

Para jogar, é necessário ter o Python 3 instalado na máquina. Além disso, você deve instalar a biblioteca pygame com o comando:

```bash
python3 -m pip install pygame
```

Após instalar a biblioteca, clone este repositório e, dentro da pasta do projeto, execute:

```bash
python3 jogo.py
```

Mantenha a pasta `assets` junto do arquivo `jogo.py`, pois ela contém as imagens, a fonte e os áudios usados pelo jogo.

O jogo será aberto em uma nova janela e pode ser jogado com os seguintes controles:

- **Enter:** iniciar a partida na tela inicial ou recomeçar na tela de game over.
- **Setas do teclado:** movimentar a nave.
- **Espaço:** atirar durante a partida.
- **Botão de fechar a janela:** sair do jogo.
