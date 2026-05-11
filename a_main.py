


# pip install magnet2torrent
#
# This script:
# 1. Look for every .magnet file in the same folder where this script is running.
# 2. Reads the magnet link from each .magnet file.
# 3. Connects to the BitTorrent network to fetch the torrent metadata.
# 4. Saves the result as a .torrent file in the same folder.
#
# Notes:
# - A magnet link does not already contain the full .torrent metadata.
# - The script must find peers/DHT sources that can provide that metadata.
# - Because of that, some conversions may fail or take time.

import asyncio
from pathlib import Path

from magnet2torrent import Magnet2Torrent, FailedToFetchException


# Convert one magnet link into one .torrent file.
async def convert_magnet_file(magnet_file: Path) -> None:
    # Read the text content of the .magnet file.
    magnet_link = magnet_file.read_text(encoding="utf-8").strip()

    # Basic validation so we skip files that do not contain a magnet URI.
    if not magnet_link.startswith("magnet:?"):
        print(f"[SKIP] {magnet_file.name} does not contain a valid magnet link")
        return

    # Output file uses the same base name, only the extension changes to .torrent.
    output_file = magnet_file.with_suffix(".torrent")

    print(f"[INFO] Converting {magnet_file.name} -> {output_file.name}")

    try:
        # Create the converter object for this magnet link.
        m2t = Magnet2Torrent(magnet_link)

        # Ask the library to fetch the torrent metadata from peers/DHT.
        filename_from_network, torrent_data = await m2t.retrieve_torrent()

        # Write the received torrent bytes to disk.
        output_file.write_bytes(torrent_data)

        print(f"[OK] Saved {output_file.name}")

        # Optional: show the name announced by the torrent metadata if available.
        if filename_from_network:
            print(f"[META] Network filename: {filename_from_network}")

    except FailedToFetchException:
        # The library could not obtain metadata for this magnet link.
        print(f"[FAIL] Could not fetch metadata for {magnet_file.name}")

    except Exception as e:
        # Catch any other unexpected error so one bad file does not stop all others.
        print(f"[ERROR] {magnet_file.name}: {e}")


# Main async entry point.
async def main() -> None:
    # Folder where the script is running.
    current_folder = Path(__file__).resolve().parent

    # Find all files with the .magnet extension in this folder only.
    magnet_files = sorted(current_folder.glob("*.magnet"))

    if not magnet_files:
        print("[INFO] No .magnet files found in this folder")
        return

    print(f"[INFO] Found {len(magnet_files)} .magnet file(s)")

    # Process the files one by one.
    # Sequential processing is simpler and easier to debug.
    for magnet_file in magnet_files:
        await convert_magnet_file(magnet_file)


# Standard Python startup block.
if __name__ == "__main__":
    asyncio.run(main())
    
    
    
