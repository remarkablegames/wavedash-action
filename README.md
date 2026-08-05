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
    permissions:
      contents: read
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Wavedash Action
        uses: remarkablemark/wavedash-action@v1
        with:
          token: ${{ secrets.WAVEDASH_TOKEN }}
```

## Usage

**Basic with a committed `wavedash.toml`:**

```yaml
- name: Wavedash Action
  uses: remarkablemark/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
```

**Auto-generate `wavedash.toml` and inject the Wavedash SDK:**

```yaml
- name: Wavedash Action
  uses: remarkablemark/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
    game-id: ${{ secrets.WAVEDASH_GAME_ID }}
    upload-dir: ./dist
    entrypoint: index.html
    sdk-version: 1.3.40
```

**Upload and publish with release notes:**

```yaml
- name: Wavedash Action
  uses: remarkablemark/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
    publish: true
    version: 1.2.3
    title: Version 1.2.3
    summary: Bug fixes and polish
    fixed: |
      Fixed fullscreen sizing
      Fixed input timing
```

## Inputs

See [action.yml](action.yml)

### `token`

**Required**. Your Wavedash API token. Store it as a repository secret (e.g., `WAVEDASH_TOKEN`).

```yaml
- uses: remarkablemark/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
```

### `config`

**Optional**. Path to `wavedash.toml`. Defaults to `./wavedash.toml`.

### `game-id`

**Optional**. Game ID used to create `wavedash.toml` when the config file does not exist. If `game-id` is provided and `config` is missing, the action writes the config file for you.

### `upload-dir`

**Optional**. Upload directory used when creating `wavedash.toml`. Defaults to `./dist`.

### `entrypoint`

**Optional**. Entrypoint used when creating `wavedash.toml` and when injecting the Wavedash SDK. Defaults to `index.html`.

### `sdk-version`

**Optional**. Wavedash SDK version injected into the entrypoint HTML when auto-creating `wavedash.toml`. Defaults to `1.3.40`.

### `publish`

**Optional**. Whether to publish the uploaded build. Defaults to `false`.

### `version`

**Optional**. Build version or message passed to `wavedash build push -m`. Defaults to `1.2.3`.

### `title`

**Optional**. Release title passed to `wavedash publish`.

### `summary`

**Optional**. Release summary passed to `wavedash publish`.

### `added`, `removed`, `fixed`, `adjusted`

**Optional**. Multiline lists of changelog items passed to `wavedash publish`. One item per line.

```yaml
- uses: remarkablemark/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
    publish: true
    added: |
      New level
      New character
    fixed: |
      Fixed crash on startup
```

## Outputs

### `build-id`

The build ID returned by `wavedash build push`.

```yaml
- uses: remarkablemark/wavedash-action@v1
  id: wavedash
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}

- run: echo "Build ID ${{ steps.wavedash.outputs.build-id }}"
```

### `playtest-url`

The playtest URL returned by `wavedash build push`.

### `published`

`true` if the build was published, otherwise `false`.

## `wavedash.toml`

Wavedash uses a `wavedash.toml` file to know which game to upload and where the built files are.

```toml
game_id = "YOUR_GAME_ID_HERE"
upload_dir = "./dist"
entrypoint = "index.html"
```

You can commit this file to your repo or let the action create it by providing `game-id`, `upload-dir`, and `entrypoint`.

## SDK injection

When the action auto-generates `wavedash.toml`, it also injects the Wavedash SDK script before the closing `</body>` tag of your entrypoint HTML. The script loads from `https://esm.sh/@wvdsh/sdk-js@<sdk-version>`.

## License

[MIT](LICENSE)
