import os
import chess
from openai import OpenAI
from stockfish import Stockfish
from random import choice
from dotenv import load_dotenv
#https://github.com/zhelyabuzhsky/stockfish/blob/master/stockfish/models.py

prefix = 'Do your best to beat me in a game of Chess. '
response_definition = 'Limit your response to moves via standard algebraic game notation. For example, your response should be no longer than this: e2e4. '
fen_definition = "I will send you the board position via fen notation. Capital letters represent white pieces and lower case letters represent black pieces. The notation's first character begins by representing the A8 square. Each following character represents B8, C8, all the way to H8 on the 8th rank. After the '/' character the following characters represent A7 through H7 sqaures of the 7th rank all the way down to the 1st rank. Any digits represent the number of empty squares on that rank before the next letter. "
previous_move_definition = 'From now on, I will send you my next move. It will be in standard algebraic notaion. For example a8c6 moves the piece on a8 to c6. If there is a piece on c6, the a8 piece will capture it. '

# set for local machine
stockfish = Stockfish(os.getenv("STOCKFISH_PATH"))
stockfish.set_depth(20)
stockfish.set_elo_rating(3500)

# NOTE !!! THESE PARAMETERS MAY NEED TO CHANGE DEPENDING ON SYSTEM RESOURCES
# This configuration is good for Surface Pro
stockfish.update_engine_parameters({
    "Threads": 4,
    "Hash": 512
})

board = chess.Board()
load_dotenv()
client = OpenAI(
    api_key=os.getenv("API_KEY"),
)

def initialize():
    global board

    board = chess.Board()

def move(move = None):
    if move: board.push_san(move)
    stockfish.set_fen_position(board.fen())

def eval():
    print(board)
    print(stockfish.get_fen_position())
    print(stockfish.get_evaluation(), '\n')

def get_Garys_move(previous_move = None, fen_mem = None, color = 'white', is_first_move = False, last_fen = None): # TODO

    color_declaration = f'You are {color}. '
    instruction = ''

    # prompt for first move
    if is_first_move:
        if previous_move:
            instruction = 'What is your first move?'
            prompt = prefix + color_declaration + response_definition + previous_move_definition + instruction
        elif fen_mem:
            instruction = 'What is your first move?'
            prompt = prefix + color_declaration + response_definition + fen_definition + instruction

    # prompt for all other moves
    else:
        if previous_move:
            instruction = f'My previous move is {previous_move}. How do you respond?'
        elif fen_mem:
            instruction = f'My previous move is represented in the board {last_fen}. How do you respond?'
        prompt = response_definition + color_declaration + instruction

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    answer = chat_completion.choices[0].message.content

    if ' ' in answer: answer = answer.split(' ')[-1]
    print("Gary's PROMPT: ", prompt)
    print("Gary's ANSWER: ", answer)
    return answer, prompt

def preview_moves(num_moves):
    moves = []
    cur_eval = stockfish.get_evaluation()
    cur_cp = cur_eval['value'] if cur_eval['type'] == 'cp' else (10000 if cur_eval['value'] > 0 else -10000)
    top_moves = stockfish.get_top_moves(num_moves)

    for move_info in top_moves:
        move = move_info['Move']
        test_board = board.copy(stack=False)
        test_board.push_uci(move)

        stockfish.set_fen_position(test_board.fen())
        test_eval = stockfish.get_evaluation()
        test_cp = test_eval['value'] if test_eval['type'] == 'cp' else (10000 if test_eval['value'] > 0 else -10000)
                
        delta_CP = test_cp - cur_cp
        captures_better_piece = None
        moves.append([delta_CP, captures_better_piece])

        print(delta_CP)

    return moves # return if the move captures a piece, CP rating (convert mate ratings to 10000/-10000), anything else useful

def get_Stocks_move(top_move=None, chance=1):
    stockfish.set_fen_position(board.fen())

    num_moves = len(list(board.legal_moves))
    move_choice = 1

    if top_move:
        move_choice = top_move

    elif chance != 1:
        move_choice = choice([i for i in range(1, 1 + chance)])
        print(f'move_choice: {move_choice}')
        if num_moves <= 2:move_choice = 1
    
    if move_choice >= num_moves:
        move_choice = 1

    try:
        move = stockfish.get_top_moves(move_choice)
    except:
        move = None
        print('Stockfish failed to find a move. Did the game end?')
    
    try:
        move = move[move_choice - 1]['Move']
    except:
        print('\n', move, "didn't work?")
    return move

def check_move(move):
    try:
        return True if board.is_legal(chess.Move.from_uci(move)) else False
    except:
        return False

# print(stockfish.get_parameters()) # Interested in UCI_Elo or target gameplay elo possible max at 3500, mid set to 1350
# print(f' Stockfish Versions: {stockfish.get_stockfish_major_version()}\n')
