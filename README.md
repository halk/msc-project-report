<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons Lizenzvertrag" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/80x15.png" /></a>

# LaTeX source code of my MSc project

## A Multi-Purpose Recommender Framework
Halil I. Köklü
Supervised by Nigel Martin

## Links

- Respective [project proposal](https://github.com/halk/msc-project-proposal)
- Resulting [projects](https://github.com/halk/recowise-vagrant)
- [Final submission](https://github.com/halk/msc-project-report/releases/download/final/PROJ_KokluH.pdf)

## Build

1. Install [MacTeX](https://tug.org/mactex/mactex-download.html).
2. Clone this repository and browse to the created directory in a terminal.
3. Run `xelatex -shell-escape index.tex`.
4. You may want to run this two or three times (so that e.g. table of content are loaded after the first compilation).
5. To re-compile bibliography, run `bibtex index.aux`. Repeat 3.

Built with source code listing

6. Uncomment `\input` tags in `sections/appendices.tex`.
7. Run

```bash
$ git submodule update --init
$ cd includes/source
$ git submodule init
$ git submodule update demo
$ git submodule update engines/inCommon
$ git submodule update engines/itemSimilarity
$ git submodule update framework
$ cd ../../scripts/parse_source
$ python parse.py
```

9. Repeat step 3.

## License

<span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">A Multi-Purpose Recommender Framework</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/halk/msc-project-report" property="cc:attributionName" rel="cc:attributionURL">Halil Köklü</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.
