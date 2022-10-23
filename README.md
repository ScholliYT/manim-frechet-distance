# Manim Fréchet distance
A [Manim](https://www.manim.community/) animated presentation of the [Fréchet distance](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance), it's use cases, variants and algorithms.


## Installation
```sh
poetry config virtualenvs.prefer-active-python true
pyenv local 3.10.6
poetry install
```


## Building the presentation

### Rendering video files with Manim
```sh
poetry run manim -qm -a --save_sections manim_frechet_distance/presentation.py
```

### Build presentation using Manim-Editor
```sh
manedit --project_name Frechet-Distance \
    --quick_present_export ./media/videos/presentation/720p30/sections/MinimalPresentationExample.json
```

### Viewing the presentation
```sh
cd ./Frechet-Distance
poetry run python3 -m http.server
```

Then open [localhost:8000](http://localhost:8000)
