# https://www.wtharvey.com/
import chess

#fen = 'r2qkb1r/pp2nppp/3p4/2pNN1B1/2BnP3/3P4/PPP2PPP/R2bK2R w KQkq - 1 0'
#fen = '1rb4r/pkPp3p/1b1P3n/1Q6/N3Pp2/8/P1P3PP/7K w - - 1 0'
fen = '3q1r1k/2p4p/1p1pBrp1/p2Pp3/2PnP3/5PP1/PP1Q2K1/5R1R w - - 1 0'
#fen = 'r5rk/2p1Nppp/3p3P/pp2p1P1/4P3/2qnPQK1/8/R6R w - - 1 0'
#fen = 'r4rk1/5pp1/1p3n1p/1Nb5/7P/1BP2Q2/5PP1/3R2K1 w - - 3 27'

b = chess.Board(fen)

value_map = [0, 1, 3, 3, 5, 9, 0]


def minimax(board, depth, alpha, beta):
    best_score = -1000 if board.turn else 1000
    best_move = None

    if depth == 0:
        score = 0
        for p in board.piece_map().values():
            color = 1 if p.color else -1
            score += (value_map[p.piece_type] * color)

        return score, None

    if board.is_checkmate():
        return -1000 if board.turn else 1000, None
    if board.is_stalemate():
        return 0, None

    for move in board.legal_moves:
        board.push(move)
        value, _ = minimax(board, depth - 1, alpha, beta)
        board.pop()

        if board.turn:
            if value > best_score:
                best_score, best_move = value, move

            if value >= beta:
                break
            alpha = max(value, alpha)

        else:
            if value < best_score:
                best_score, best_move = value, move

            if value <= alpha:
                break
            beta = min(value, beta)

    return best_score, best_move

def chess_ai(board):
    return minimax(board, 6, -1000, 1000)


score, move = chess_ai(b)
print(f'{b.san(move)}: {score}')
#print(score)
