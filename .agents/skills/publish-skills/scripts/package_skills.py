#!/usr/bin/env python3
"""Package every skill directory containing SKILL.md into dist/*.zip."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def discover_skills(skills_directory):
    """Return direct child directories that contain a SKILL.md file."""
    skills_directory = Path(skills_directory)
    return sorted(
        (
            directory
            for directory in skills_directory.iterdir()
            if directory.is_dir() and (directory / "SKILL.md").is_file()
        ),
        key=lambda directory: directory.name,
    )


def package_skill(skill_directory, output_directory):
    """Create a ZIP whose root is the skill directory's contents."""
    skill_directory = Path(skill_directory)
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    archive_path = output_directory / f"{skill_directory.name}.zip"

    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(skill_directory.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(skill_directory).as_posix())

    return archive_path


def main():
    repository_root = next(
        (
            directory
            for directory in Path(__file__).resolve().parents
            if (directory / "skills").is_dir() and (directory / "AGENTS.md").is_file()
        ),
        None,
    )
    if repository_root is None:
        raise SystemExit("Could not locate the repository root from the script path")

    skills_directory = repository_root / "skills"
    output_directory = repository_root / "dist"

    if not skills_directory.is_dir():
        raise SystemExit(f"Skills directory not found: {skills_directory}")

    skills = discover_skills(skills_directory)
    if not skills:
        raise SystemExit(f"No skill directories containing SKILL.md found in {skills_directory}")

    archives = [package_skill(skill_directory, output_directory) for skill_directory in skills]

    # Remove obsolete packages only after every current skill was packaged successfully.
    expected_names = {archive.name for archive in archives}
    for archive in output_directory.glob("*.zip"):
        if archive.is_file() and archive.name not in expected_names:
            archive.unlink()

    for archive in archives:
        print(archive)


if __name__ == "__main__":
    main()
