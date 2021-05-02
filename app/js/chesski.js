
const blackCastleSquares = ["g8", "c8"];
const whiteCastleSquares = ["g1", "c1"]

function isPromotion(piece, targetSquare) {
    let color = piece[0];
    let pieceName = piece[1];
    if (pieceName !== 'P') {
        return false;
    }
    if (color === 'b' && targetSquare[1] === "1") {
        return true;
    } else if (targetSquare[1] === "8") {
        return true;
    }
}

function isCastle(piece, sourceSquare, targetSquare) {
    let color = piece[0];
    let pieceName = piece[1];
    if (pieceName !== 'K') {
        return false;
    }
    if (color === 'b' && sourceSquare === 'e8' && blackCastleSquares.includes(targetSquare)) {
        return true;
    }
    if (color === 'w' && sourceSquare === 'e1' && whiteCastleSquares.includes(targetSquare)) {
        return true;
    }
}

function movePieceToPosition(board, start, end, pieceInfo) {
    let positionObject = board.position();
    delete positionObject[start];
    positionObject[end] = pieceInfo;
    board.position(positionObject);
}

function replacePiece(board, square, piece) {
    let positionObject = board.position();
    delete positionObject[square];
    positionObject[square] = piece;
    board.position(positionObject);
}

function castleRook(board, targetSquare) {
    if (targetSquare === 'g1') {
        movePieceToPosition(board, "h1", "f1", "wR");
        return;
    }
    if (targetSquare === "c1") {
        movePieceToPosition(board, "a1", "d1", "wR");
        return;
    }
    if (targetSquare === "g8") {
        movePieceToPosition(board, "h8", "f8", "bR");
    }
    if (targetSquare === "c8") {
        movePieceToPosition(board, "a8", "d8", "bR");
    }
}

// TODO - Add function perform castle