git clone -b release/0.30 --recurse-submodules https://github.com/LeelaChessZero/lc0.git
cd lc0
./build.sh
pip install -e .
cd ..
pip install -r requirements.txt
