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

        conda env export | grep -v "^prefix: " > environment.yml

        conda env export --no-builds | grep -v "^prefix: " > environment_no_builds.yml

        conda env export --from-history | grep -v "^prefix: " > environment_from_history.yml
