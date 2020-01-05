# Meow refactor

Refactoring task, original at [link](https://github.com/somnoynadno/meow_hero)

## Set up environment

Install Miniconda, then
```
conda env create -f environment.yml -n <env_name>
conda activate <env_name>
cd <project_root>/src
```

## Run game

```
python main.py
```

## Run tests

### Run all
```
python -m tests
```
### Run separately
```
python -m tests.<test_module>
```

> # Meow Hero
> 
> The game about cat, who study on "Software engineering" program in TSU.
> 
> ## Developers: 
> - Alexander Zorkin (programming) 
> - Rufina Rafikova (plot and music)
> - Anastasia Politova (design)
> 
> ## Installation
> ### Linux
> 
> 1. Download or clone the repo to your working directory.
> 
>         git clone https://github.com/somnoynadno/meow_hero.git
> 2. Move to project directory
> 
>         cd meow_hero
> 3. Install game requirements
> 
>         pip3 install -r requirements.txt
> 4. Start the main script
> 
>         python3 src/main.py
>         
> ### Windows
> 
> Sorry, we have not executable file, so you need to follow this instruction:
> 
> 0. Make sure you have the latest version of Python3 and pip installed in your system. If not, install it by following instruction https://python-scripts.com/install-python-windows. 
> Be sure to check the box for "Add Python X. Y to PATH" in the configuration wizard! 
> 
> 1. Download zip and extract project to your working directory.
> 
> 2. Open project directory in cmd. If you have troubles with this step: https://nastroyvse.ru/opersys/win/sozdat-papku-cherez-komandnuyu-stroku-windows.html.
> 
> 3. Install game requirements
> 
>         pip install -r requirements.txt
>         
> 4. Start the main script
> 
>         python src/main.py
>         
> or by double click on main script in /src directory.
> 
> ### Troubleshooting
> 
> If you have any troubles with installation and google can't help, just write me in vk: https://vk.com/somnoynadno.
> 
> ## Enjoy!
