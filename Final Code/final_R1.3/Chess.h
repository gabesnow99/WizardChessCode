//Chess.h

#ifndef Chess_h
#define Chess_h

#include "C:\Users\joshu\Documents\Personal\Projects worth doing\Chess\WizardChessCode\Final Code\final_R1.3\Definitions.h"
#include <Arduino.h>

struct Square {
  char file;
  char rank;
  int x;
  int y;

  Square() : file('A'), rank('1'), x(0), y(0) {}
  Square(char file, char rank) : file(file), rank(rank),
                                x(HALF_WALL_LENGTH + int(file - 'A') * WALL_LENGTH),
                                y(HALF_WALL_LENGTH + int(rank - '1') * WALL_LENGTH) {}
};

class Piece {
public:
    Piece(char file, char rank) : _currentSquare(file, rank),
                                  _index(StoI(_currentSquare)) {}

    Square getSquare() {
      return _currentSquare;
    }

    int getIndex() {
      return _index;
    }

    void moveTo(Square newSquare) {
      // TODO: CHECK FOR AND HANDLE A KILL. MAY NEED A BOARD LIST
      _currentSquare = newSquare;
      _index = StoI(_currentSquare);
    }

private:
    Square _currentSquare;
    int _index;
    int StoI(Square square) {
      int fileIndex = square.file - 'A';
      int rankIndex = square.rank - '1';
      int index = rankIndex * 8 + fileIndex;
      return index;
    }
};

// TODO: CREATE FUNCTION movePiece() THAT MOVES A PIECE LOCATED AT ONE SQUARE TO ANOTHER SQUARE AND CHECKS IF THERE EVEN IS A PIECE THERE OR NOT AND IF A KILL IS NECESSARY
// TODO: SEE IF python_prototype.py HAS ANY ADDITIONAL FUNCTIONALITY
// TODO: CHANGE Chess.h to Piece.h AND MAKE ANOTHER Chess.h THAT INCLUDES ALL DEFINITIONS AND FUNCTIONS IN THE .ino FILE 

int StoI(Square square) {
  int fileIndex = square.file - 'A';
  int rankIndex = square.rank - '1';
  int index = rankIndex * 8 + fileIndex;
  return index;
}

Square ItoS(int index) {
  char file = 'A' + index % 8;
  char rank = '1' + index / 8;
  Square square = Square(file, rank);
  return square;
}

Square UserInputSquare() {
  int index = 0;
  int count = 0;
  char serial[2] = {'0'};
  
  delay(100);

  if (Serial.available() <= 0) {return;}

  while (Serial.available() > 0) {
    serial[index] = char(Serial.read());
    index++;
    count++;
    if (count >= 2) { break; }
  }
  while (Serial.available() > 0) {Serial.read();}

  Square square = Square(serial[0], serial[1]);
  return square;
}

#endif
