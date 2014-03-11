

## First , set up the environment path

    BoxesPath=/Workspace/python_projects/Boxes/

    export PYTHONPATH="$HOME$BoxesPath"



## Second , clone the project (skip if u have cloned)

    git clone https://github.com/isaacselement/Boxes.git "$HOME$BoxesPath"



## Third , run it
    
    python "$PYTHONPATH"App/script/application.py

    
## For short :
    BoxesPath=/Workspace/python_projects/Boxes/ \ 
    && export PYTHONPATH="$HOME$BoxesPath" \ 
    && python "$PYTHONPATH"App/script/application.py
    
    or just run ./startServer.sh
