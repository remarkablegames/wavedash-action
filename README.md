# wavedash-action

[![GitHub Release](https://img.shields.io/github/v/release/remarkablegames/wavedash-action)](https://github.com/remarkablegames/wavedash-action/releases)
[![test](https://github.com/remarkablegames/wavedash-action/actions/workflows/test.yml/badge.svg)](https://github.com/remarkablegames/wavedash-action/actions/workflows/test.yml)
[![lint](https://github.com/remarkablegames/wavedash-action/actions/workflows/lint.yml/badge.svg)](https://github.com/remarkablegames/wavedash-action/actions/workflows/lint.yml)

〰️ Upload and publish your game files to [Wavedash](https://wavedash.com/).

## Quick Start

```yaml
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      # Build your web game...

      - name: Upload to Wavedash
        uses: remarkablegames/wavedash-action@v2
        with:
          token: ${{ secrets.WAVEDASH_TOKEN }}
```

## Usage

If you have a `wavedash.toml`:

```yaml
- name: Upload to Wavedash
  uses: remarkablegames/wavedash-action@v2
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
```

If you don't have a `wavedash.toml`:

```yaml
- name: Upload to Wavedash
  uses: remarkablegames/wavedash-action@v2
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
    game-id: ${{ secrets.WAVEDASH_GAME_ID }}
    upload-dir: ./dist
    entrypoint: index.html
```

> The action will create the config and inject the Wavedash init script into your entrypoint.

Upload and publish with release notes:

```yaml
- name: Upload and publish to Wavedash
  uses: remarkablegames/wavedash-action@v2
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
- uses: remarkablegames/wavedash-action@v2
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
```

### `config`

**Optional**. Path to `wavedash.toml`. Defaults to `wavedash.toml`.

### `game-id`

**Optional**. Game ID from the Developer Portal. If `game-id` is provided and `config` is missing, the action creates `wavedash.toml` for you.

### `upload-dir`

**Optional**. Path to your built game files. Defaults to `./dist`.

### `entrypoint`

**Optional**. The first file Wavedash loads inside `upload-dir`. Defaults to `index.html`.

### `inject-init`

**Optional**. Whether to inject the Wavedash init script. Defaults to `true`. Set to `false` if your game calls `Wavedash.init()`:

```yaml
- uses: remarkablegames/wavedash-action@v2
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
    inject-init: false
```

### `cache`

**Optional**. Whether to cache the Wavedash CLI. Defaults to `true`.

### `publish`

**Optional**. Whether to publish the uploaded build. Defaults to `false`.

### `build-message`

**Optional**. Build message passed to `wavedash build push -m`.

### `publish-title`

**Optional**. Release title passed to `wavedash publish`.

### `publish-summary`

**Optional**. Release summary passed to `wavedash publish`.

### `publish-added`, `publish-removed`, `publish-fixed`, `publish-adjusted`

**Optional**. Multiline lists of changelog items passed to `wavedash publish`:

```yaml
- uses: remarkablegames/wavedash-action@v2
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

Build ID returned by `wavedash build push`.

```yaml
- uses: remarkablegames/wavedash-action@v2
  id: wavedash
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}

- run: echo "Build ID ${{ steps.wavedash.outputs.build-id }}"
```

### `playtest-url`

Playtest URL returned by `wavedash build push`.

### `published`

`true` if the build was published, otherwise `false`.

## `wavedash.toml`

Wavedash uses a [config](https://docs.wavedash.com/cli/configuration) file to know which game to upload and where the built files are:

```toml
game_id = "YOUR_GAME_ID_HERE"
upload_dir = "./dist"
entrypoint = "index.html"
```

> When your `wavedash.toml` has `upload_dir` or `entrypoint`, those values are used. The action inputs `upload-dir` and `entrypoint` only apply when the key is missing.

## Wavedash init

`window.Wavedash` is available before your game starts so the action injects a script into your entrypoint:

```javascript
window.Wavedash&&(Wavedash.updateLoadProgressZeroToOne(1),Wavedash.init());
```

If `Wavedash.init()` isn't called, your game is blocked behind a loading screen. To update the load progress, set [`inject-init`](#inject-init) to `false` and call:

```javascript
Wavedash.updateLoadProgressZeroToOne(0);
// load assets...
Wavedash.updateLoadProgressZeroToOne(1);
Wavedash.init();
```

> Injection is skipped when `Wavedash.init()` appears in your upload directory. The `entrypoint` must be an HTML or JavaScript file, otherwise the action fails.

## Migration

### v2

v2 removes the `sdk-version` input and stops downloading `@wvdsh/sdk-js`:

```diff
- uses: remarkablegames/wavedash-action@v1
+ uses: remarkablegames/wavedash-action@v2
  with:
    token: ${{ secrets.WAVEDASH_TOKEN }}
-   sdk-version: 1.3.54
```

The action now injects `window.Wavedash.init()` and adds the [`inject-init`](#inject-init) input.

## License

[MIT](LICENSE)
