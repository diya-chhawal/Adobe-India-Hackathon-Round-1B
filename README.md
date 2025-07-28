# Adobe Hackathon Round 1B

## Build

```bash
docker build --platform linux/amd64 -t mysolution:round1b .
```

## Run

```bash
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none mysolution:round1b
```

Put your PDFs in `input/`. The JSON output will appear in `output/`.