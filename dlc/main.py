# Stub example game.
def main():
    """
    Main example function.

    Returns:
        nothing
    """
    # Trigger the example window code.
    a = gamelib.open("dlc/game.w")
    print("\n\n")
    b = a.read()
    print(b)
    a.close()
    print("\n\n")
    c = gamelib.loadmod("dlc/mod.py")
    c.main()
    config = gamelib.phrase(b.splitlines())
    print("\n\n")
    gamelib.debug("Example debug")
    gamelib.warn("Example warning")
    gamelib.error("example error")
    gamelib.info("Hello from example game")
    gamelib.exwindow()
    gamelib.info("Goodbye from example game")