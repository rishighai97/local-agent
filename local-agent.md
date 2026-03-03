# install llama.cpp on ubuntu
## If you decide to build llama.cpp your self, I recommend you to use their official manual at: https://github.com/ggerganov/llama.cpp/blob/master/docs/build.md

## You may need to install some packages:

sudo apt update
sudo apt install build-essential
sudo apt install cmake
sudo apt install libcurl4-openssl-dev

## Download and build llama.cpp:

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release

## what is llama.cpp
https://blog.steelph0enix.dev/posts/llama-cpp-guide/

# llama.cpp client location
/home/rishighai/llama.cpp/build/bin

# ollama
- wrapper over llama.cpp
- used to install llama models
- setup - https://ollama.com/download/linux

# ollama model location (downloaded ollama llama 2 7b parameters model)
- select sha file whose size matches with the output of the command - ollama list
/usr/share/ollama/.ollama/models/blobs/
sha256-667b0c1932bc6ffc593ed1d03f895bf2dc8dc6df21db3042284a6f4416b06a29 

# run llama cpp cli client
./home/rishighai/llama.cpp/build/bin/llama-cli -m /usr/share/ollama/.ollama/models/blobs/sha256-667b0c1932bc6ffc593ed1d03f895bf2dc8dc6df21db3042284a6f4416b06a29 

# run llama server (open ai compatible) using hugging face so that we can connect agent to it
- added step in llama-server.sh file
./home/rishighai/llama.cpp/build/bin/llama-server --port 8091 -hf unsloth/Phi-4-mini-instruct-GGUF
- open terminal in project root and run - ./llama-server.sh

# run llama server with hugging face model


# open ai agent docs
https://openai.github.io/openai-agents-python/

