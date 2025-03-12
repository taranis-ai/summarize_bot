# Taranis AI Summarize Bot

This code takes stories in the format as provided by [Taranis AI](https://github.com/taranis-ai/taranis-ai) and summariezes them.

## Development

```bash
uv venv
uv sync --all-extras --dev
```

## Usage

Run via

```bash
flask run
# or
granian app
# or
docker run -p 8000:8000 ghcr.io/taranis-ai/taranis-summarize-bot:latest
```

### Example API Call

To test the API with a POST request, use curl:

```bash
curl -X POST http://127.0.0.1:8000/ \
  -H "Content-Type: application/json" \
  -d '{"text": "This is an example sentence to summarize."}'
```


## License

EUROPEAN UNION PUBLIC LICENCE v. 1.2

