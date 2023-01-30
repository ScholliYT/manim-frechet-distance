[![wakatime](https://wakatime.com/badge/user/13925bfd-efdd-4399-ae64-d0247d6b76cb/project/d0f656e0-a9b0-4e38-b646-03cf5851b931.svg)](https://wakatime.com/badge/user/13925bfd-efdd-4399-ae64-d0247d6b76cb/project/d0f656e0-a9b0-4e38-b646-03cf5851b931)

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
    --quick_present_export ./media/videos/presentation/720p30/sections/Titlepage.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/Motivation.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/DistanceOfCurves.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/ProblemsWithHausdorffDistance.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/FrechetDistanceIntro.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/DiscreteFrechetDistanceIntro.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/ComputingTheFrechetDistance.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/FreeSpaceCell.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/FreeSpaceDiagram.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/FrechetDistanceAlgorithmicComplexity.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/DiscreteFrechetDistanceAlgorithm.json \
    --quick_present_export ./media/videos/presentation/720p30/sections/DiscreteFrechetDistanceAlgorithmicComplexity.json
```

### 3. Viewing the presentation
```sh
cd ./Fréchet-Distance/
poetry run python3 -m http.server
```

Then open [localhost:8000](http://localhost:8000)


# Credits
Some images used in the presentation are from external sources as noted below.
- [Crane Bird](https://icons8.com/icon/mgTrUgOfGUva/crane-bird) icon by [Icons8](https://icons8.com)
- [Person Pointing](https://icons8.com/icon/HHppGuDxwFp0/person-pointing) icon by [Icons8](https://icons8.com)
- [Dog Jump](https://icons8.com/icon/GZSZiebXkvbw/dog-jump) icon by [Icons8](https://icons8.com)
- [Frog](https://icons8.com/icon/103359/frog) icon by [Icons8](https://icons8.com)
