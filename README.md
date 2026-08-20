# wavedash-action

[![GitHub Release](https://img.shields.io/github/v/release/remarkablegames/wavedash-action)](https://github.com/remarkablegames/wavedash-action/releases)
[![test](https://github.com/remarkablegames/wavedash-action/actions/workflows/test.yml/badge.svg)](https://github.com/remarkablegames/wavedash-action/actions/workflows/test.yml)
[![lint](https://github.com/remarkablegames/wavedash-action/actions/workflows/lint.yml/badge.svg)](https://github.com/remarkablegames/wavedash-action/actions/workflows/lint.yml)

〰️ Upload and publish your game files to [Wavedash](https://wavedash.com/).

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

      # Build your web game...

      - name: Upload to Wavedash
        uses: remarkablegames/wavedash-action@v1
        with:
          token: ${{ secrets.WAVEDASH_TOKEN }}
```

## Usage

If you have a `wavedash.toml`:

```yaml
- name: Upload to Wavedash
  uses: remarkablegames/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
```

If you don't have a `wavedash.toml`, then the action will create one for you and inject the Wavedash SDK into your entrypoint HTML:

```yaml
- name: Upload to Wavedash
  uses: remarkablegames/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
    game-id: ${{ secrets.WAVEDASH_GAME_ID }}
    upload-dir: ./dist
    entrypoint: index.html
    sdk-version: 1.3.45
```

Upload and publish with release notes:

```yaml
- name: Upload and publish to Wavedash
  uses: remarkablegames/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
    publish: true
    build-message: Bug fixes and polish
    publish-title: Version 1.2.3
    publish-summary: Bug fixes and polish
    publish-fixed: |
      Fixed fullscreen sizing
      Fixed input timing
```

## Inputs

See [action.yml](action.yml)

### `token`

**Required**. Your Wavedash API token. Store it as a repository secret (e.g., `WAVEDASH_TOKEN`).

```yaml
- uses: remarkablegames/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
```

### `config`

**Optional**. Path to `wavedash.toml`. Defaults to `wavedash.toml`.

### `game-id`

**Optional**. Game ID used to create `wavedash.toml` when the config file does not exist. If `game-id` is provided and `config` is missing, the action writes the config file for you.

### `upload-dir`

**Optional**. Upload directory used when creating `wavedash.toml`. Defaults to `./dist`.

### `entrypoint`

**Optional**. Entrypoint used when creating `wavedash.toml` and when injecting the Wavedash SDK. Defaults to `index.html`.

### `sdk-version`

**Optional**. Wavedash SDK version injected into the entrypoint HTML when auto-creating `wavedash.toml`. Defaults to `1.3.45`.

### `cache`

**Optional**. Whether to cache the installed Wavedash CLI between runs, keyed by runner OS and CLI version. Defaults to `true`.

### `publish`

**Optional**. Whether to publish the uploaded build. Defaults to `false`.

### `build-message`

**Optional**. Build message passed to `wavedash build push -m`.

### `publish-title`

**Optional**. Release title passed to `wavedash publish`.

### `publish-summary`

**Optional**. Release summary passed to `wavedash publish`.

### `publish-added`, `publish-removed`, `publish-fixed`, `publish-adjusted`

**Optional**. Multiline lists of changelog items passed to `wavedash publish`. One item per line.

```yaml
- uses: remarkablegames/wavedash-action@v1
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
    publish: true
    publish-added: |
      New level
      New character
    publish-fixed: |
      Fixed crash on startup
```

## Outputs

### `build-id`

The build ID returned by `wavedash build push`.

```yaml
- uses: remarkablegames/wavedash-action@v1
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

When the action auto-generates `wavedash.toml`, it also injects the Wavedash SDK into your entrypoint HTML. A `<link rel="modulepreload">` is added before the closing `</head>` tag to start fetching the module early, and the SDK script is added before the closing `</body>` tag to initialize Wavedash. The SDK loads from `https://esm.sh/@wvdsh/sdk-js@<sdk-version>`.

## License

[MIT](LICENSE)
