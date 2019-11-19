# Bootstrapping Files

## Training a Sentiment Model

### Building the Training Image

Model training is handled via a custom Docker container. In order to produce this container run:

```shell script
bazel run //services/streaming/bin:model_training
```

This will produce a Docker image named `fnwclient_streaming_model_training` with the tag `latest` on the local system.

### General Syntax

Now that we've built the container we will use it using the following general syntax.

```shell script
docker run -ti --rm \
  -e NVIDIA_VISIBLE_DEVICES=all \
  --runtime=nvidia \
  -v <host training data path>:<container training data path> \
  -v <host output path>:<container output path> \
  fnwclient_streaming_model_training:latest \
  <opts>
```

The container supports the following options.

| Option | Description | Example |
|---------|------------|---------|
| --rootdir | Path to data set root directory _in the container_. | "/opt/data/input" |
| --outdir| Path to model output directory _in the container_. | "/opt/data/output" |
| --train | Training dataset file name (without path) | "train.txt" |
| --dev| Dev dataset file name (without path) | "dev.txt" |
| --test| Test dataset file name (without path) | "test.txt" |
| --epochs| Maximum number of Epochs| 25 |
| --device | Compute device to use| "cuda:0" |

To find out which compute devices are valid on your system run `docker run -ti --rm <image>:<tag> --help`, which will display
something similar to the following

```text
Train a flair model to be used with the streaming analytics module.

optional arguments:
  -h, --help            show this help message and exit
  --rootdir ROOTDIR     Dataset path
  --outdir OUTDIR       Path to put output files
  --train TRAIN         Training set filename
  --dev DEV             Dev set filename
  --test TEST           Test/validation set filename
  --epochs EPOCHS       Number of epochs
  --device {cpu,cuda:0} Which compute device to use
```

The options listed under `--device` are valid compute devices. In this example we can use "cpu" or "cuda:0".

### Pitfalls

If only "cpu" is listed under `--device` then a few things might be at play:

* The Nvidia runtime isn't installed
* The host system isn't equipped with a GPU
* The hosy system doesn't have a CUDA-compatible GPU
* `torch` doesn't recognized the GPU

### Example Usage

Lets assume we are in a directory with the following structure.
```text
.
├── data_set
│       ├── test.txt
│       ├── train.txt
│       └── dev.txt
└── output
```

Where `test.txt`, `train.txt`, and `dev.txt` are datasets in in Flair friendly format.

Then we would run the following command to train a model using the training container built earlier.

```shell script
docker run -ti --rm \
    -e NVIDIA_VISIBLE_DEVICES=all \
    --runtime=nvidia \
    -v ./data_set:/opt/data/input \
    -v ./output:/opt/data/output \
    train_sentiment_model:latest \
    --rootdir "/opt/data/input" \
    --outdir "/opt/data/output"  \
    --train "train.txt" \
    --dev "dev.txt" \
    --test "test.txt" \
    --epochs 25 \
    --device "cuda:0"
```

## Getting a Validated Telegram Session