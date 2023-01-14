# Manim Presentation on Fréchet Distance
A [Manim](https://www.manim.community/) animated presentation of the [Fréchet distance](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance), it's use cases, variants and algorithms.

## Docs

Besides the presentaion there is also a written essay [here](https://nightly.link/ScholliYT/manim-frechet-distance/workflows/build_docs/main/PDF.zip).


## Installation

Install all dependencies of manim as described here: https://docs.manim.community/en/stable/installation/linux.html#required-dependencies

```sh
poetry config virtualenvs.prefer-active-python true # in case your system python is < 3.10
pyenv local 3.10.6
poetry install
```


## Building the presentation

### 1. Rendering video files with Manim
```sh
poetry run manim -qm -a --save_sections manim_frechet_distance/presentation.py
```

### 2. Build presentation using Manim-Editor
```sh
poetry run manedit --project_name Fréchet-Distance \
    --quick_present_export ./media/videos/presentation/720p30/sections/MinimalPresentationExample.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/BraceAnnotation.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/HausdorffDistance.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/ArgMinExample.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/FrechetDistanceExample.json
```

### 3. Viewing the presentation
```sh
cd ./Fréchet-Distance/
poetry run python3 -m http.server
```

Then open [localhost:8000](http://localhost:8000)
