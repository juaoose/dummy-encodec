# FastAPI EnCodec compression

## build

```bash
docker build -t encodec .
```

## run

```bash
docker run -p 8081:80 -d encodec
```

## Sample request

```bash
curl -v -F "file=@sample.wav" http://localhost:8000 -O -J
```
Note that the result is a `.ecdc` file.

## Compared to the CLI

This would return the compressed file, like running this command:

```bash
encodec --hq -r -f sample.wav
```

If you want to decompress it, you can use:

```bash
encodec --hq -r -f response.ecdc file.wav
```
