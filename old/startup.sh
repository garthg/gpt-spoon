mkdir local-gpt || true
cd local-gpt
here=$(pwd)

model=gpt4all-lora-quantized.bin

cd $here
if [ ! -d gpt4all ]; then
    git clone https://github.com/nomic-ai/gpt4all.git
fi

cd $here
cd gpt4all
cd chat
if [ ! -f $model ]; then
    curl https://the-eye.eu/public/AI/models/nomic-ai/gpt4all/$model > $model
fi

cd $here
if [ ! -d pyllamacpp ]; then
    git clone --recursive https://github.com/nomic-ai/pyllamacpp && cd pyllamacpp
    cd pyllamacpp
    pip3 install --user .
fi

cd $here
mkdir converted-model || true
cd converted-model
if [ ! -f tokenizer.model ]; then
    echo "You need the huggingface model. Go to https://huggingface.co/decapoda-research/llama-7b-hf/tree/main and get tokenizer.model and put it at $(pwd)/tokenizer.model"
    exit 1
fi
export PATH=/Users/gwg/Library/Python/3.9/bin:$PATH  # TODO this should happen elsewhere?
pyllamacpp-convert-gpt4all ${here}/gpt4all/chat/$model tokenizer.model converted-${model}


#pip3 install --user nomic  # deprecated, also only linux x86 or ARM
