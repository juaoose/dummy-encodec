# gpt on azure

## build

```bash
docker build -t azuregpt .
```

## run

```bash
docker run -p 5000:7860 -e OPENAI_API_KEY='' azuregpt
```
