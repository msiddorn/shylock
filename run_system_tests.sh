# start local server
python3 app.py 9555 &
server_pid=$!

# always kill server
trap 'kill $server_pid' EXIT SIGINT

for file in tests/system/test_*.py; do
    py.test "$file"
done
