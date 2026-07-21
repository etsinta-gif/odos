import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS = [
    "Starter_Pack_1.1",
    "Starter_Pack_1.2",
    "Starter_Pack_1.3",
    "Starter_Pack_1.4",
    "Starter_Pack_1.5",
]

if __name__ == "__main__":
    output_dir = ROOT / "starter_packs_zips"
    output_dir.mkdir(exist_ok=True)

    for pack in PACKS:
        pack_dir = ROOT / pack
        if not pack_dir.exists():
            print(f"Skipping missing pack: {pack}")
            continue
        zip_path = output_dir / f"{pack}.zip"
        if zip_path.exists():
            zip_path.unlink()
        shutil.make_archive(str(zip_path.with_suffix("")), "zip", pack_dir)
        print(f"Created {zip_path}")
