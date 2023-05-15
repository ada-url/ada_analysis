if [ ! -d "boost_1_82_0" ]; then
  wget https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.tar.gz
  tar xzvf boost_1_82_0.tar.gz
fi
cd boost_1_82_0
./bootstrap.sh
sudo ./b2 install
cd ..

if [ ! -d "url-various-datasets" ]; then
  git clone https://github.com/ada-url/url-various-datasets
fi


sudo apt-get update
sudo apt-get install  -y rustc cargo
cmake -DADA_BOOST_URL=ON -DADA_BENCHMARKS=ON -B build
cmake --build build -j

for file in $(find url-various-datasets | grep txt); do jsonname=$(basename $file .txt).json;./build/benchmarks/benchdata $file --benchmark_out_format=json --benchmark_out=$jsonname  ; echo $jsonname; done
