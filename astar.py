import chess
import heapq
import sys
import time
import numpy as np

class Astar:



    def __init__(self, fen_string):
        self.ind = 0
        self.depth = int(fen_string[-1])
        self.fen = fen_string[:-1] + 'KQkq - 0 1'
        self.enemyPlayer = chess.BLACK if fen_string.split(" ")[1] == "w" else chess.WHITE
        self.player = chess.BLACK if self.enemyPlayer == chess.WHITE else chess.WHITE
        self.king = self.get_king_area()


    def run_astar(self):
        # run astar algorithm
        seen = set()
        pq = []
        heapq.heapify(pq)
        t = time.time()
        state = chess.Board()
        state.set_fen(self.fen)
        heapq.heappush(pq, (0, self.ind, state))
        self.ind += 1
        end_move = -1
        seen.add(state.fen().split(" ")[0])
        while pq and end_move == -1:
            state = heapq.heappop(pq)[2]
            if (time.time() - t > 20.0):
                return "TIMEOUT"
            for move in state.legal_moves:
                currentDepth = len(state.move_stack)//2 + 1
                state.push(move)
                currentFen = state.fen().split(" ")[0]
                if state.is_checkmate() and currentDepth == self.depth:
                    end_move = state
                    break
                # check if check # check if check mate and not 0 moves
                if state.is_check() or state.is_checkmate() and currentDepth < self.depth or \
                        currentDepth >= self.depth or currentFen in seen:
                    seen.add(currentFen)
                    state.pop()
                    continue
                if not currentFen in seen:
                    seen.add(currentFen)
                    state.push(chess.Move.null())
                    heapq.heappush(pq, (self.heuristic(state), self.ind, state.copy()))
                    self.ind += 1
                    state.pop()
                    state.pop()
        return self.constructString(end_move) if end_move != -1 else "No Solution Found"


    def constructString(self, state):
        s = ""
        for move in state.move_stack:
            mv = str(move)
            s += mv[:2]+"-"+mv[2:]+";" if move != chess.Move.null() else ""
        return s[:-1]

    def covering(self, state):
        # covering heuristic
        score = 0
        for field in self.king:
            score += len(state.attackers(self.player, field))
        score += 4*len(state.attackers(self.player, state.king(self.enemyPlayer)))
        return -score


    def manhattan(self, state):
        pieces = chess.PAWN, chess.KING, chess.BISHOP, chess.ROOK, chess.KNIGHT, chess.QUEEN
        d = 0
        for p in pieces:
            for sq_pos in state.pieces(p, self.player):
                d += min([chess.square_distance(sq_pos, field) for field in self.king])
        return d

    def heuristic(self, state):
        return self.covering(state) + 1*len(state.move_stack) + 0.2*self.manhattan(state)

    def get_king_area(self):
        board = chess.Board()
        board.set_fen(self.fen)
        allPos = board.attacks(board.king(self.enemyPlayer))
        return allPos

if __name__ == '__main__':
    # get file name
    fileName = ""
    fen = ""
    try:
        fileName = sys.argv[1]
        with open(fileName, "rt") as f:
            fen = f.readline()
    except Exception:
        print("index error")

    algorithm = Astar(fen)
    solution = algorithm.run_astar()
    print(solution)
