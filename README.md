# wavedash-action

[![GitHub Release](https://img.shields.io/github/v/release/remarkablegames/wavedash-action)](https://github.com/remarkablegames/wavedash-action/releases)
[![test](https://github.com/remarkablegames/wavedash-action/actions/workflows/test.yml/badge.svg)](https://github.com/remarkablegames/wavedash-action/actions/workflows/test.yml)
[![lint](https://github.com/remarkablegames/wavedash-action/actions/workflows/lint.yml/badge.svg)](https://github.com/remarkablegames/wavedash-action/actions/workflows/lint.yml)

〰️ Upload and publish your game files to Wavedash.

## Quick Start

```yaml
on: push
jobs:
  wavedash-action:
    runs-on: ubuntu-latest
    steps:
      - name: Wavedash Action
        uses: remarkablemark/wavedash-action@v1
```

## Usage

**Basic:**

```yaml
- uses: remarkablemark/wavedash-action@v1
```

See [action.yml](action.yml)

## Inputs

### `version`

**Optional**: The version. Defaults to `1.2.3`:

```yaml
- uses: remarkablemark/wavedash-action@v1
  with:
    version: 1.2.3
```

## License

[MIT](LICENSE)
