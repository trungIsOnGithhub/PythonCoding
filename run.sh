if [ $# == 1 ]; then
    source "$1/bin/activate"
    python3 "$1/script.py"
fi