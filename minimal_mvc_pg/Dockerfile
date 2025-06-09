FROM python:3.11-slim

WORKDIR /code

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -r <(pip install --dry-run . | awk '/^\s+-/ {print $2}')

# Copy application code
COPY . .

# Copy CSV files (these must exist in your project directory)
COPY AAPL.csv /code/AAPL.csv
COPY MSFT.csv /code/MSFT.csv

# Expose Flask port
EXPOSE 5000

# Run Flask app
ENTRYPOINT ["./entrypoint.sh"]
