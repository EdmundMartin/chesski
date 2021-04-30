
const blackCastleSquares = ["g8", "c8"];
const whiteCastleSquares = ["g1", "c1"]

function isPromotion(color, piece, targetSquare) {
    if (piece !== 'p') {
        return false;
    }
    if (color === 'b' && targetSquare[1] === "1") {
        return true;
    } else if (targetSquare[1] === "8") {
        return true;
    }
}

function isCastle(color, piece, sourceSquare, targetSquare) {
    if (piece !== 'k') {
        return false;
    }
    let spacesMoved = Math.abs(Number(sourceSquare[1]) - Number(targetSquare[1]))
    if (spacesMoved !== 2) {
        return false;
    }
    if (color === 'b' && blackCastleSquares.includes(targetSquare)) {
        return true;
    }
    if (color === 'w' && whiteCastleSquares.includes(targetSquare)) {
        return true;
    }
}

// TODO - Add function perform castle