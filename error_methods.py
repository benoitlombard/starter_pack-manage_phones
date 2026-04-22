import typer
"""
I made the following choices concerning handling errors:
- firstly, we always announce every success or failure to user through color printing with 'typer.secho(message, color)'
      failure message try to be as precise as possible.
- if CLI is used :
    when its possible, we raise the related exception, otherwise we return True for success and False for failure.
- if menu version is used :
    we never raise exceptions, and we return True for success and False for failure, sub function is exited and user can retry from main menu.
"""

def error_printing(message: str, is_success: bool)->None:
    """
    Print error/success message formatted RED/GREEN using Typer module.\n
    parameter of function: 'is_success' defines the color of the output True= Green (success), False= Red (failure)
    """
    if is_success:
        typer.secho(message, fg=typer.colors.GREEN)
    else:
        typer.secho(message, fg=typer.colors.RED)
