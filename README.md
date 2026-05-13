


# magnet-to-torrent

Small script to turn `.magnet` files in the current folder into `.torrent` files using the `magnet2torrent` library.

---

## What it does

- Scans the script folder for `*.magnet` files.
- Reads each file, expecting a single `magnet:?` URI.
- Uses `magnet2torrent` to fetch torrent metadata from peers/DHT.
- Writes a matching `.torrent` file next to each `.magnet` file.

Example:

```text
movie.magnet  ->  movie.torrent
```

---

## Requirements

- Python 3.8+
- Package: `magnet2torrent`  (`pip install magnet2torrent`)  
  This library handles connecting to the BitTorrent network and retrieving metadata from peers.

---

## Usage

1. Install dependency:

   ```bash
   pip install magnet2torrent
   ```

2. Save the script as (for example):

   ```text
   a_main.py
   ```

3. In the same folder, create one or more files ending with `.magnet`, each containing a single magnet link:

   ```text
   myfile.magnet   # content: magnet:?xt=urn:btih:...
   ```

4. Run:

   ```bash
   python a_main.py
   ```

5. If metadata is found, you will get corresponding `.torrent` files in the same folder.

---

## Behavior and limitations

- Only `.magnet` files in the script’s directory are processed (no recursion).
- A file is skipped if its content does not start with `magnet:?`.
- Conversion can fail or take a long time if no peers/DHT nodes provide metadata for that magnet.
- Network availability and torrent health determine success; the script cannot force peers to exist.
