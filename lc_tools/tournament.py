import chess
from itertools import permutations
from .match import play_match
from ._opening_book import play_from_opening_book
from tqdm import tqdm

def _get_match_id(p1, p2, round_id):
    """Return a unique integer for each pair of p1 and p2 for every value of round_id.

    Property:
        _get_match_id(p1, p2, r) == _get_match_id(p2, p1, r) for all p1, p2, r
    """
    return hash("".join(sorted(str(p1) + str(p2) + str(round_id))))

def _get_board(opening_book, repeat, opening_book_depth, white, black, round_count):
    if opening_book:
        if repeat:
            return play_from_opening_book(
                opening_book,
                max_depth=opening_book_depth,
                random_seed=_get_match_id(white, black, round_count),
            )
        else:
            return play_from_opening_book(
                opening_book, max_depth=opening_book_depth
            )
    else:
        return chess.Board()

def _parse_result(result: str):
    """Parse the result string from a chess.Board instance and return a tuple of win, loss and draw counts.

    Arguments
    ---------
    result: str
        The result string from a chess.Board instance.

    Returns
    -------
    Tuple of win, loss and draw counts.
    """
    if result == "1-0":
        return 1, 0, 0
    elif result == "0-1":
        return 0, 1, 0
    elif result == "1/2-1/2":
        return 0, 0, 1
    else:
        raise ValueError(f"Unknown result string: {result}")


def play_tournament(
    players,
    n_games=1,
    opening_book=None,
    opening_book_depth=10,
    repeat=True,
):
    """Play all possible matches between the given players.

    Each possible matchup, including white/black permutations, will be played `n_games` times each.

    Arguments
    ---------
    players: list of str
        A list of executables of the UCI engines to play.
    n_games: int
        The number of times each match-up should be played.
    opening_book: str, optional
        If the openings should be selected from an opening book, give the
        path to a polyglot opening book as this parameter. Default is to not
        use a book.
    opening_book_depth: int, optional
        Maximum depth to play out from the `opening_book`. Has no effect if no book is given.
        Default is a depth of 10 (20 plies).
    repeat: bool, optional
        When using an opening book, setting this to True will ensure that
        each player plays both sides of the same opening vs the same opponent.
        Default value is True.

    Returns
    -------
        Tuple of win, loss and draw counts for each player. 
    """
    assert len(players) > 1, "At least two players are required!"
    names = set([p.name for p in players])
    assert len(names) == len(players), "All players must have unique names."

    results = dict({p: {"win": 0, "loss": 0, "draw": 0} for p in players})
    for round_count in range(1, n_games + 1):
        perms = list(permutations(players, 2))
        for white, black in tqdm(perms, desc=f"Round {round_count}/{n_games}"):
            board = _get_board(opening_book, repeat, opening_book_depth, white, black, round_count)
            result = play_match(
                white,
                black,
                fen=board.fen(),
                return_board=False
            )
            win, loss, draw = _parse_result(result)
            
            results[white]["win"] += win
            results[white]["loss"] += loss
            results[white]["draw"] += draw
            results[black]["win"] += loss
            results[black]["loss"] += win
            results[black]["draw"] += draw

    # assert that the sum of wins, losses and draws are equal for all players
    wins = sum([results[p]["win"] for p in players])
    losses = sum([results[p]["loss"] for p in players])
    assert wins == losses, f"Total wins and losses are not equal: {wins} != {losses}"
    draws = sum([results[p]["draw"] for p in players])
    assert (wins + losses + draws)/2 == n_games * len(players) * (len(players) - 1), f"Total games played not equal to expected: {int((wins + losses + draws)/2)} != {n_games * len(players) * (len(players) - 1)}"

    return results