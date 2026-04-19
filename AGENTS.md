# Agents Directory

This document provides an overview of the browser-use agents implemented in this repository.

## Browser-Use Documentation

For AI agents, use this documentation to understand how to use the browser-use-sdk: https://docs.browser-use.com/llms-full.txt

## Current Agents

### 1. Top Movies Agent (`top_movies.py`)
- **Purpose**: Automates the task of searching and compiling a list of anticipated new movie releases for a given year.
- **Tools & Capabilities**: Uses `browser-use-sdk` to search the web, extract data, and summarize it into a compact list.
- **Execution**: `uv run top_movies.py`

### 2. Top Amazon Products Agent (`top_amazon.py`)
- **Purpose**: Asks the user for a product to search, then finds the top 5 most popular products matching the input on Amazon, along with their product rating and current price.
- **Tools & Capabilities**: Uses `browser-use-sdk` to search Amazon, extract product data, and summarize ratings and prices into a formatted response.
- **Execution**: `uv run top_amazon.py`

### 3. Gmail Inbox Checker Agent (`gmail.py`)
- **Purpose**: Automates logging into Gmail (using persistent custom profiles) and checks the inbox for emails matching specific criteria (e.g., from 'Google'), extracting their subject, sender, and timestamp.
- **Tools & Capabilities**: Uses `browser-use-sdk` streaming, multi-step tasks across a persistent session, and data extraction from web applications.
- **Execution**: `uv run gmail.py`
