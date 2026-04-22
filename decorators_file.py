import typer
import time

def decorator_timer(original_function):
    """
    This function is a decorator that add measurement of delay of execution of a function\n
    Delay is printed using typer.secho() and BRIGHT_BLACK police.
    """
    def wrapper_function(*args, **kwargs):
        if True:
            time_origin = time.time()
        ret =  original_function(*args, **kwargs)

        if True:
            typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
        return ret
    return wrapper_function
