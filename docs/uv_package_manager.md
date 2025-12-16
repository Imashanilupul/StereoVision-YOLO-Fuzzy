# UV Package Manager Guide

UV is an extremely fast Python package installer and resolver, written in Rust. It's designed as a drop-in replacement for pip and pip-tools.

## Installation

### Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Using pip
```bash
pip install uv
```

## Basic Commands

### Installing Packages

```bash
# Install a single package
uv pip install numpy

# Install multiple packages
uv pip install numpy pandas matplotlib

# Install from requirements.txt
uv pip install -r requirements.txt

# Install specific version
uv pip install "numpy==1.24.0"

# Install with version constraints
uv pip install "numpy>=1.20,<2.0"
```

### Creating and Managing Virtual Environments

```bash
# Create a virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.11

# Create in a specific directory
uv venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (Linux/macOS)
source .venv/bin/activate
```

### Uninstalling Packages

```bash
# Uninstall a package
uv pip uninstall numpy

# Uninstall multiple packages
uv pip uninstall numpy pandas matplotlib
```

### Listing Installed Packages

```bash
# List all installed packages
uv pip list

# Show package information
uv pip show numpy

# List outdated packages
uv pip list --outdated
```

### Freezing Dependencies

```bash
# Generate requirements.txt with exact versions
uv pip freeze > requirements.txt

# Compile requirements.in to requirements.txt
uv pip compile requirements.in -o requirements.txt

# Compile with upgrade
uv pip compile requirements.in -o requirements.txt --upgrade
```

### Syncing Dependencies

```bash
# Install exact dependencies from requirements.txt
uv pip sync requirements.txt

# Sync will uninstall packages not in requirements.txt
```

## Project Workflow

### Setting Up a New Project

```bash
# 1. Create project directory
mkdir my-project
cd my-project

# 2. Create virtual environment
uv venv

# 3. Activate virtual environment (Windows)
.venv\Scripts\activate

# 4. Install dependencies
uv pip install -r requirements.txt
```

### Managing Dependencies

```bash
# Create requirements.in with top-level dependencies
echo "numpy" > requirements.in
echo "pandas" > requirements.in
echo "matplotlib" > requirements.in

# Compile to requirements.txt with locked versions
uv pip compile requirements.in -o requirements.txt

# Install dependencies
uv pip sync requirements.txt
```

### Updating Dependencies

```bash
# Update all packages
uv pip compile requirements.in -o requirements.txt --upgrade

# Update specific package
uv pip compile requirements.in -o requirements.txt --upgrade-package numpy

# Sync after update
uv pip sync requirements.txt
```

## Advanced Usage

### Working with pyproject.toml

```bash
# Install project dependencies from pyproject.toml
uv pip install -e .

# Install with optional dependencies
uv pip install -e ".[dev]"
```

### Cache Management

```bash
# Show cache directory
uv cache dir

# Clean cache
uv cache clean
```

### Using UV with Different Python Versions

```bash
# Create venv with Python 3.10
uv venv --python 3.10

# Create venv with Python 3.11
uv venv --python 3.11

# Use specific Python executable
uv venv --python /path/to/python
```

## UV vs Pip Comparison

| Command | pip | uv |
|---------|-----|-----|
| Install package | `pip install numpy` | `uv pip install numpy` |
| Install from requirements | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| Compile dependencies | `pip-compile requirements.in` | `uv pip compile requirements.in` |
| Sync dependencies | `pip-sync requirements.txt` | `uv pip sync requirements.txt` |
| Create venv | `python -m venv .venv` | `uv venv` |

## Performance Benefits

- **10-100x faster** than pip for package installation
- Parallel downloads and installations
- Efficient dependency resolution
- Smart caching mechanism

## Tips and Best Practices

1. **Use `requirements.in` for top-level dependencies** and `uv pip compile` to generate locked `requirements.txt`
2. **Use `uv pip sync`** instead of `uv pip install -r` for reproducible environments
3. **Keep UV updated** for best performance: `uv self update`
4. **Use virtual environments** to isolate project dependencies
5. **Commit both `requirements.in` and `requirements.txt`** to version control

## Common Workflows for This Project

### Initial Setup
```bash
# Clone repository
cd c:\Users\User\OneDrive\Documents\GitHub\StereoVision-YOLO-Fuzzy

# Create virtual environment
uv venv

# Activate environment (Windows)
.venv\Scripts\activate

# Install dependencies from pyproject.toml
uv pip install -e .
```

### Adding New Dependencies
```bash
# Add to pyproject.toml dependencies, then:
uv pip install -e .

# Or install directly
uv pip install opencv-python
```

### Updating Dependencies
```bash
# Update all packages
uv pip install --upgrade -e .
```

## Troubleshooting

### UV Command Not Found
```bash
# Add UV to PATH or use full path
# Windows: Add %USERPROFILE%\.cargo\bin to PATH
```

### Virtual Environment Not Activating
```bash
# Windows: Ensure execution policy allows scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use: .venv\Scripts\Activate.ps1
```

### Package Installation Fails
```bash
# Clear cache and retry
uv cache clean
uv pip install <package>
```

## Additional Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [UV Installation Guide](https://github.com/astral-sh/uv#installation)
- [Python Packaging Guide](https://packaging.python.org/)
