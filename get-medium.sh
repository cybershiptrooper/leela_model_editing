mkdir -p nets
wget https://storage.lczero.org/files/networks-contrib/t1-512x15x8h-distilled-swa-3395000.pb.gz
./lc0/build/release/lc0 leela2onnx --input="nets/t1-512x15x8h-distilled-swa-3395000.pb.gz" --output="../../../nets/512_filters_model.onnx"
