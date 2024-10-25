import math


# Inicializar el tablero de 4x4
def create_board():
    return [[' ' for _ in range(4)] for _ in range(4)]


# Imprimir el tablero
def print_board(board):
    print("    0   1   2   3")
    print("  -----------------")
    for i, row in enumerate(board):
        print(f"{i} | " + " | ".join(row) + " |")
        print("  -----------------")


# Comprobar si hay ganador
def check_win(board, player):
    # Comprobar filas, columnas y diagonales
    for i in range(4):
        if all([cell == player for cell in board[i]]):  # Filas
            return True
        if all([board[j][i] == player for j in range(4)]):  # Columnas
            return True
    # Diagonales
    if all([board[i][i] == player for i in range(4)]):
        return True
    if all([board[i][3 - i] == player for i in range(4)]):
        return True
    return False


# Comprobar si hay empate
def check_draw(board):
    return all([cell != ' ' for row in board for cell in row])


# Función de evaluación heurística
def evaluate(board):
    if check_win(board, 'X'):
        return 1
    elif check_win(board, 'O'):
        return -1
    else:
        return 0


# Minimax con poda alfa-beta
def minimax(board, depth, is_maximizing, alpha, beta):
    score = evaluate(board)

    # Si hay un ganador o empate, devolver la evaluación
    if score == 1 or score == -1:
        return score
    if check_draw(board):
        return 0

    # Maximizar el jugador IA (X)
    if is_maximizing:
        max_eval = -math.inf
        for i in range(4):
            for j in range(4):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    # Minimizar el jugador oponente (O)
    else:
        min_eval = math.inf
        for i in range(4):
            for j in range(4):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval


# Encontrar la mejor jugada para la IA
def best_move(board):
    best_val = -math.inf
    move = (-1, -1)

    for i in range(4):
        for j in range(4):
            if board[i][j] == ' ':
                board[i][j] = 'X'  # IA juega con 'X'
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                print(f"Evaluando movimiento en ({i}, {j}) con valor: {move_val}")  # Depuración
                board[i][j] = ' '  # Deshacer movimiento
                if move_val > best_val:
                    move = (i, j)
                    best_val = move_val
    print(f"Mejor movimiento encontrado en: {move} con valor {best_val}")  # Depuración
    return move


# Modalidades del juego
def play_game():
    board = create_board()
    mode = input("Elige el modo (1: Humano vs Humano, 2: Humano vs IA, 3: IA vs IA): ")

    if mode == '1':
        # Humano vs Humano
        current_player = 'X'
        while True:
            print_board(board)
            row = int(input(f"Jugador {current_player}, elige fila (0-3): "))
            col = int(input(f"Jugador {current_player}, elige columna (0-3): "))
            if board[row][col] == ' ':
                board[row][col] = current_player
                if check_win(board, current_player):
                    print_board(board)
                    print(f"Jugador {current_player} gana!")
                    break
                if check_draw(board):
                    print_board(board)
                    print("Empate!")
                    break
                current_player = 'O' if current_player == 'X' else 'X'
            else:
                print("Movimiento inválido, intenta de nuevo.")

    elif mode == '2':
        # Humano vs IA
        while True:
            print_board(board)
            # Turno del jugador humano
            row = int(input("Elige fila (0-3): "))
            col = int(input("Elige columna (0-3): "))
            if board[row][col] == ' ':
                board[row][col] = 'O'
                if check_win(board, 'O'):
                    print_board(board)
                    print("¡Has ganado!")
                    break
                if check_draw(board):
                    print_board(board)
                    print("Empate!")
                    break

                # Turno de la IA
                print("Turno de la IA...")
                move = best_move(board)
                if move != (-1, -1):  # Verificar si se encontró un movimiento válido
                    board[move[0]][move[1]] = 'X'
                else:
                    print("Error: no se encontró un movimiento para la IA")
                if check_win(board, 'X'):
                    print_board(board)
                    print("La IA gana!")
                    break
                if check_draw(board):
                    print_board(board)
                    print("Empate!")
                    break
            else:
                print("Movimiento inválido, intenta de nuevo.")

    elif mode == '3':
        # IA vs IA
        current_player = 'X'
        while True:
            print_board(board)
            print(f"Turno de la IA ({current_player})...")
            move = best_move(board)
            if move != (-1, -1):  # Verificar si se encontró un movimiento válido
                board[move[0]][move[1]] = current_player
            else:
                print("Error: no se encontró un movimiento para la IA")
            if check_win(board, current_player):
                print_board(board)
                print(f"La IA ({current_player}) gana!")
                break
            if check_draw(board):
                print_board(board)
                print("Empate!")
                break
            current_player = 'O' if current_player == 'X' else 'X'


# Iniciar el juego
play_game()
