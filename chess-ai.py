#!/usr/bin/env python

import chess
import chess.polyglot

class BlueRose:
    def __init__(self):
        self.opening_book = chess.polyglot.open_reader("Titans.bin")
        self.board = chess.Board()
        self.value_map = [0, 1, 3, 3, 5, 9, 0]

    def minimax(self, depth, alpha, beta):
        if self.board.is_checkmate():
            return -100 if self.board.turn else 100, None
        if self.board.is_stalemate():
            return 0, None

        if depth == 0:
            score = 0
            for p in self.board.piece_map().values():
                color = 1 if p.color else -1
                score += (self.value_map[p.piece_type] * color)

            return score, None

        best_score = -100 if self.board.turn else 100
        best_move = None

        for move in self.board.legal_moves:
            board.push(move)
            value, _ = self.minimax(depth - 1, alpha, beta)
            board.pop()

            if self.board.turn:
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

    def ai(self, depth):
        try:
            move = self.opening_book.weighted_choice(self.board).move
            score = 0
        except IndexError:
            score, move = self.minimax(depth, -100, 100)

        return score, move

    def uci(self, command):
        if command == 'uci':
            print('id name BlueRose 1')
            print('id author Brian Pomerantz')
            print('uciok')

        elif command == 'isready':
            print('readyok')

        elif command == 'ucinewgame':
            self.board = chess.Board()

        elif 'position' in command:
            args = command.split()
            fen = args[1]
            if fen == 'startpos':
                fen = chess.STARTING_FEN

            self.board = chess.Board(fen)

        elif 'go' in command:
            score, move = self.ai(6)
            print(f'info score {score*100}')
            print(f'bestmove {self.board.uci(move)}')

        elif command == 'quit':
            return 1

        return 0

if __name__ == '__main__':
    engine = BlueRose()
    result = 0
    while result == 0:
        uci_input = input()
        result = engine.uci(uci_input)
