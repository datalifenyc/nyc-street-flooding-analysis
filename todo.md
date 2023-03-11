# Project Checklist

## File Storage

- [X] Activate Git Large File Storage and assess deploymnet impact
- [ ] Integrate DVC for PLUTO & MapPLUTO datasets
- [ ] Create utilities function to delete old street flooding datasets, after new data has been successfully downloaded
- [ ] Check file space before downloading files
- [X] Create destination folder if it does not exist
- [ ] Create input dialog for type of PLUTO or MapPLUTO dataset to download

## Documentation

- [ ] Add details about installation in README
- [ ] Add files description table in ABOUT page of Jupyter Book
- [ ] Add datasets description table in ABOUT page of Jupyter Book

## Pre-commit actions

- [ ] Update `environment.yml` libraries

        conda env export | grep -v "^prefix: " > environment-with-builds.yml

        conda env export --no-builds | grep -v "^prefix: " > environment-no-builds.yml

        conda env export --from-history | grep -v "^prefix: " > environment.yml

## Troubleshoot

- [ ] Fix Google Colab "Notebook loading error" - `SyntaxError: JSON.parse: unexpected character at line 1 column 1 of the JSON data`

        [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datalifenyc/nyc-street-flooding-analysis/blob/main/analysis-book/obtain-flood-data.ipynb)
