# Manim Presentation on Fréchet Distance
A [Manim](https://www.manim.community/) animated presentation of the [Fréchet distance](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance), it's use cases, variants and algorithms.


## Installation

Install all dependencies of manim as described here: https://docs.manim.community/en/stable/installation/linux.html#required-dependencies

```sh
poetry config virtualenvs.prefer-active-python true # in case your system python is < 3.10
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
poetry run manedit --project_name Frechet-Distance \
    --quick_present_export ./media/videos/presentation/720p30/sections/MinimalPresentationExample.json
```

### Viewing the presentation
```sh
cd ./Frechet-Distance
poetry run python3 -m http.server
```

Then open [localhost:8000](http://localhost:8000)