# hello-browser-use
trying out browser-use

## Setup Environment

This project uses `uv` for fast Python dependency management.

1. **Install uv** (if you haven't already):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   *(For other installation methods, refer to the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).)*

2. **Set up your environment variables**:
   Copy from `.env.example` to create a `.env` file in the root directory to store your API keys necessary for the `browser-use-sdk` to operate (such as your `BROWSER_USE_API_KEY`).
   ```bash
   cp .env.example .env
   ```

3. **Install dependencies**:
   Run the following command to automatically create a virtual environment (`.venv`) and install all required packages listed in `pyproject.toml`:
   ```bash
   uv sync
   ```

## Running the Examples

Once the environment is successfully initialized and your `.env` is configured, you can run the example scripts!

To run the `top_movies.py` example, use:
```bash
uv run top_movies.py
```

*(Alternatively, you can manually activate the environment with `source .venv/bin/activate` and run `python top_movies.py`)*
