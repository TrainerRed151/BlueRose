using Chess
using Chess.Book


#fen = "r2qkb1r/pp2nppp/3p4/2pNN1B1/2BnP3/3P4/PPP2PPP/R2bK2R w KQkq - 1 0"
#fen = "1rb4r/pkPp3p/1b1P3n/1Q6/N3Pp2/8/P1P3PP/7K w - - 1 0"
#fen = "3q1r1k/2p4p/1p1pBrp1/p2Pp3/2PnP3/5PP1/PP1Q2K1/5R1R w - - 1 0"
#fen = "r5rk/2p1Nppp/3p3P/pp2p1P1/4P3/2qnPQK1/8/R6R w - - 1 0"
#fen = "r4rk1/5pp1/1p3n1p/1Nb5/7P/1BP2Q2/5PP1/3R2K1 w - - 3 27"
fen = "r4rk1/1bp1qppp/2p5/p1B5/1PQ5/8/P1P2PPP/R4RK1 b - - 1 0"

b = fromfen(fen)
#global b = startboard()

function minimax(board, depth, alpha, beta)
    if ischeckmate(board)
        return sidetomove(board) == WHITE ? -100 : 100, nothing

    elseif isstalemate(board)
        return 0, nothing

    elseif depth == 0
        score = 0

        score += squarecount(pawns(board, WHITE))
        score += squarecount(knights(board, WHITE))*3
        score += squarecount(bishops(board, WHITE))*3
        score += squarecount(rooks(board, WHITE))*5
        score += squarecount(queens(board, WHITE))*9

        score -= squarecount(pawns(board, BLACK))
        score -= squarecount(knights(board, BLACK))*3
        score -= squarecount(bishops(board, BLACK))*3
        score -= squarecount(rooks(board, BLACK))*5
        score -= squarecount(queens(board, BLACK))*9
        
        return score, nothing

    else
        best_score = sidetomove(board) == WHITE ? -101 : 101
        best_move = nothing

        for move in moves(board)
            #if depth == 8 && occursin("K", movetosan(board, move))
            #    continue
            #end

            u = domove!(board, move)
            value, _ = minimax(board, depth - 1, alpha, beta)
            undomove!(board, u)

            if sidetomove(board) == WHITE
                if value > best_score
                    best_score, best_move = value, move
                end

                if value >= beta
                    break
                end

                alpha = max(value, alpha)

            else
                if value < best_score
                    best_score, best_move = value, move
                end

                if value <= alpha
                    break
                end

                beta = min(value, beta)
            end
        end

        return best_score, best_move
    end
end

function ai()
    opening_move = pickbookmove(b)
    if opening_move == nothing
        score, move = minimax(b, 6, -100, 100)
        println("$(movetosan(b, move)): $score")
        domove!(b, move)
    else
        println("$(movetosan(b, opening_move)): Book move")
        domove!(b, opening_move)
    end
    println(b)
end

function me(move)
    domove!(b, move)
    println(b)
    if isstalemate(b)
        println("Stalemate")
    elseif ischeckmate(b)
        println("Checkmate")
    else
        @time ai()
    end
end

@time ai()
