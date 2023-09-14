#!/usr/bin/env python

import chess
#import chess.polyglot
import time
import sys

MAX_SCORE = 100

class BlueRose:
    def __init__(self):
        #self.opening_book = chess.polyglot.open_reader("Titans.bin")
        self.board = chess.Board()
        self.value_map = [0, 1, 3, 3, 5, 9, 0]

    def negamax(self, depth, alpha, beta, time_limit):
        if time.time() > time_limit:
            return None, None, 0

        if self.board.is_checkmate():
            score = MAX_SCORE if self.board.turn else -MAX_SCORE
            return score, None, 1

        if self.board.is_stalemate():
            return 0, None, 1

        if depth == 0:
            score = 0
            for p in self.board.piece_map().values():
                color = 1 if p.color else -1
                score += (self.value_map[p.piece_type] * color)

            if not self.board.turn:
                score = -score

            return score, None, 1

        best_score = -MAX_SCORE - 1
        best_move = None

        nodes = 0
        for move in self.board.legal_moves:
            self.board.push(move)
            value, _, new_nodes = self.negamax(depth - 1, -beta, -alpha, time_limit)
            self.board.pop()

            nodes += new_nodes

            if value is None:
                return None, None, nodes

            value = -value
            if value > best_score:
                best_score, best_move = value, move

            alpha = max(value, alpha)
            if alpha >= beta:
                break

        return best_score, best_move, nodes

    def ai(self, move_time):
        '''
        try:
            move = self.opening_book.weighted_choice(self.board).move
            score = 0
        except IndexError:
            score, move = self.minimax(depth, -100, 100)
        '''
        t1 = time.time()
        time_limit = t1 + move_time
        depth = 1
        color = [-1, 1][self.board.turn]
        best_score, best_move, nodes = self.negamax(depth, -MAX_SCORE, MAX_SCORE, time_limit)
        best_score *= color

        time_ms = int((time.time() - t1) * 1000)
        nps = int(nodes/time_ms * 1000)
        print(f'info depth 1 multipv 1 score cp {100*best_score} nodes {nodes} nps {nps} time {time_ms} pv {self.board.uci(best_move)}', flush=True)

        while True:
            if best_score == color*MAX_SCORE:
                return best_score, best_move

            depth += 1
            new_score, new_move, new_nodes = self.negamax(depth, -MAX_SCORE, MAX_SCORE, time_limit)
            nodes += new_nodes

            if new_score is None:
                break

            best_score = color*new_score
            best_move = new_move

            time_ms = int((time.time() - t1) * 1000)
            nps = int(nodes/time_ms * 1000)
            print(f'info depth {depth} multipv 1 score cp {100*best_score} nodes {nodes} nps {nps} time {time_ms} pv {self.board.uci(best_move)}', flush=True)

        return best_score, best_move

    def uci(self, command):
        if command == 'uci':
            print('id name BlueRose 1', flush=True)
            print('id author Brian Pomerantz', flush=True)
            print('uciok', flush=True)

        elif command == 'isready':
            print('readyok', flush=True)

        elif command == 'ucinewgame':
            self.board = chess.Board()

        elif 'position' in command:
            args = command.split()
            fen = args[1]
            if fen == 'startpos':
                fen = chess.STARTING_FEN

            self.board = chess.Board(fen)

            if len(args) > 2 and args[2] == 'moves':
                for move in args[3:]:
                    move_obj = chess.Move.from_uci(move)
                    self.board.push(move_obj)

        elif 'go' in command:
            score, move = self.ai(10)
            print(f'bestmove {self.board.uci(move)}', flush=True)

        elif command == 'quit':
            return 1

        return 0

if __name__ == '__main__':
    engine = BlueRose()
    result = 0
    print('BlueRose 1 by Brian Pomerantz', flush=True)
    f = open('uci.log', 'w')
    while result == 0:
        uci_input = input()
        f.write(f'{uci_input}\n')
        try:
            result = engine.uci(uci_input)
        except Exception e:
            f.write(e)
            f.close()
