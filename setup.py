from cx_Freeze import setup, Executable

executables = [Executable('main.py')]

# Define the setup configuration
setup(
    name="FlapBird GAME",
    version="1.0",
    description="A Flappy Bird style game built with Pygame",
    options={"build_exe": {"packages": ["pygame"], }},
    executables=executables,
)
