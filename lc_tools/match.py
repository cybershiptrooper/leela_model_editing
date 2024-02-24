import chess
import chess.engine
import chess.pgn
import datetime


def play_match(
    engine1,
    engine2,
    fen=chess.STARTING_FEN,
    return_board=False,
    verbose=False,
):
    """Play a match between the given engines with a given time control.

    Arguments
    ---------
    engine1, engine2: str
        Executable of the UCI engines to play. Engine1 will play white.
    fen: str, optional
        Starting position in FEN notation. Default is the standard opening position.
    engine1_options, engine2_options: dict, optional
        A dictionary with options to set for each engine. The key should be the
        name of the option as provided by the engine. To see available options you may
        do:
        ``` python
        engine = chess.engine.SimpleEngine.popen_uci("name-of-executable")
        print(engine.options)
        ```
        See https://python-chess.readthedocs.io/en/latest/engine.html#chess.engine.EngineProtocol.options

        Only the options that match the engines option names will be configured.

    Returns
    -------
        A `chess.pgn.Game` instance describing the game.
    """

    board = chess.Board(fen)
    current_player = engine1 if board.turn == chess.WHITE else engine2
    while not board.is_game_over():
        output = current_player.play(
            board,
        )
        board.push(output)
        if verbose:
            print(output, end=",")
        current_player = engine1 if board.turn == chess.WHITE else engine2
    if return_board:
        return board
    return board.result()
