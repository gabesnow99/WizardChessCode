#define BOARD_HEIGHT 3648 // == NUM_ROWS * WALL_LENGTH !!!
#define NUM_COLS 8
#define NUM_ROWS 8
#define WALL_LENGTH 456 // == BOARD HEIGHT / NUM_ROWS  !!!
#define HALF_WALL_LENGTH 228 // == WALL_LENGTH / 2     !!!
#define NUM_PIECES 32

#define WR1 0
#define WN1 1
#define WB1 2
#define WK 3
#define WQ 4
#define WB2 5
#define WN2 6
#define WR2 7
#define WP1 8
#define WP2 9
#define WP3 10
#define WP4 11
#define WP5 12
#define WP6 13
#define WP7 14
#define WP8 15
#define BP1 16
#define BP2 17
#define BP3 18
#define BP4 19
#define BP5 20
#define BP6 21
#define BP7 22
#define BP8 23
#define BR1 24
#define BN1 25
#define BB1 26
#define BK 27
#define BQ 28
#define BB2 29
#define BN2 30
#define BR2 31

//         REFERENCE TO BOARD LOCATIONS
//    ---------------------------------------
// 8 | 56 | 57 | 58 | 59 | 60 | 61 | 62 | 63 |
//    ------------------------------------ ---
// 7 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 |
//    ---------------------------------------
// 6 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 |
//    ---------------------------------------
// 5 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 |
//    ---------------------------------------
// 4 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 |
//    ---------------------------------------
// 3 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
//    ---------------------------------------
// 2 | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 |
//    ---------------------------------------
// 1 | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  |
//    ---------------------------------------
//     A    B    C    D    E    F    G    H
