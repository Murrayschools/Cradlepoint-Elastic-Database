cd "$(dirname "$0")"

echo "$PWD"

# set this to false to make
# the operating system cancel
# running the application
run=true

if [ "$run" = true ] ; then
    source ./.venv/bin/activate
    python app.py
fi