# Going Beyond EDA: A Deeper Analysis of NYC 311 Street Flooding Complaints 📈

The objective of this presentation is to examine multiple approaches for gaining deeper insights and a better understanding of the [NYC 311 Street Flood Complaints](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9) open data.

[![Jupyter Book Badge](https://jupyterbook.org/badge.svg)](https://nyc-street-flooding-analysis.datalife.nyc) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/datalifenyc/nyc-street-flooding-analysis/main?labpath=analysis-book%2F) ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/datalifenyc/nyc-street-flooding-analysis/github-actions-upload-to-gcp-storage.yml)

## Event Details 📅

__NYC Open Data Website:__ [NYC Open Data Week 2023](https://www.open-data.nyc/)

__Date:__ [Saturday, March 18, 2023 🕘](https://nycsodata23.sched.com/event/1JUZQ/going-beyond-eda-a-deeper-analysis-of-nyc-311-street-flooding-complaints)

__Analysis Book:__ [nyc-street-flooding-analysis.datalife.nyc](https://nyc-street-flooding-analysis.datalife.nyc)

## Contributors 💻

| Presenter | LinkedIn | GitHub | Twitter |
| --------- | -------- | ------ | ------- |
| Ho Hsieh | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/hohsieh) | [![GitHub followers](https://img.shields.io/github/followers/hohsieh?style=social)](https://github.com/hohsieh) | |
| Nathan Williamson | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/nathan-williamson-b0a15a122) | [![GitHub followers](https://img.shields.io/github/followers/nateswill?style=social)](https://github.com/nateswill) | |
| Mark Bauer | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/markebauer) | [![GitHub followers](https://img.shields.io/github/followers/mebauer?style=social)](https://github.com/mebauer) | [![Twitter Follow](https://img.shields.io/twitter/follow/markbauerwater?style=social)](https://twitter.com/markbauerwater) |
| Chidi Ezeolu | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/chidi-ezeolu-411b0856) | [![GitHub followers](https://img.shields.io/github/followers/datalifenyc?style=social)](https://github.com/datalifenyc)| |

## Installation 💽

### Application Installs

1. Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) to manage Python packages and environments.

2. Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to maintain version control.

3. Install [Graphviz](https://graphviz.gitlab.io/download/) to build diagrams with code.

### Terminal Commands

1. Clone [nyc-street-flood-analysis](https://github.com/datalifenyc/nyc-street-flood-analysis) repo

    ```bash
    git clone https://github.com/datalifenyc/nyc-street-flood-analysis.git
    ```

2. Enter folder directory of local repo

    ```bash
    cd nyc-street-flood-analysis
    ```

3. Install requirements

    ```bash
    conda env create -f environment.yml
    ```

    Two alternative environment files are provided, which offer detailed library versions (`environment-no-builds.yml`) and build info (`environment-with-builds.yml`).

4. Activate conda environment

    ```bash
    conda activate nyc-street-flood-analysis
    ```

5. Install and Configure Git to track large notebook files

    | Step 1: [Install](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)   | Step 2: [Configure](https://docs.github.com/en/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage)         |
    | ----------------- | ------------------------- |
    | `git lfs install` | `git lfs track "*.ipynb"` |

    Jupyter Notebooks with maps tend to larger in size. For best practices and to avoid commit warning/errors, as well as, issues pushing repo to GitHub,
    use Git Large File Storage (Git LFS): [website](https://git-lfs.com/) | [docs](https://docs.github.com/en/repositories/working-with-files/managing-large-files) | [repo](https://github.com/git-lfs/git-lfs).

    To `push` lfs updates to repo, enter:

    ```bash
    git lfs push origin main
    ```

## Notes

Jupyter Notebooks can be found in the [analysis-book](analysis-book/) folder.
