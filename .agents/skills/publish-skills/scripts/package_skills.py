#!/usr/bin/env python3
"""Package every skill directory containing SKILL.md into dist/*.zip."""

import re
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


def read_version(skill_directory):
    """Read a filename-safe version from the skill's front matter."""
    skill_file = Path(skill_directory) / "SKILL.md"
    lines = skill_file.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{skill_file}: missing front matter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError(f"{skill_file}: unterminated front matter") from None

    versions = [line.partition(":")[2].strip() for line in lines[1:end]
                if re.match(r"^version\s*:", line)]
    if len(versions) != 1:
        raise ValueError(f"{skill_file}: expected exactly one version")
    version = versions[0]
    if len(version) >= 2 and version[0] in "\"'" and version[-1] == version[0]:
        version = version[1:-1]
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9._+\-]*[A-Za-z0-9])?", version):
        raise ValueError(f"{skill_file}: invalid or empty version {version!r}")
    return version


def package_skill(skill_directory, output_directory, version):
    """Create a ZIP whose root is the skill directory's contents."""
    skill_directory = Path(skill_directory)
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    archive_path = output_directory / f"{skill_directory.name}-{version}.zip"

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

    try:
        versions = [read_version(skill_directory) for skill_directory in skills]
    except (OSError, UnicodeError, ValueError) as error:
        raise SystemExit(str(error)) from error

    archive_names = [f"{skill.name}-{version}.zip" for skill, version in zip(skills, versions)]
    if len({name.casefold() for name in archive_names}) != len(archive_names):
        raise SystemExit("Skill archive names collide")
    archives = [package_skill(skill, output_directory, version)
                for skill, version in zip(skills, versions)]

    # Remove obsolete packages only after every current skill was packaged successfully.
    expected_names = {archive.name for archive in archives}
    for archive in output_directory.glob("*.zip"):
        if archive.is_file() and archive.name not in expected_names:
            archive.unlink()

    for archive in archives:
        print(archive)


if __name__ == "__main__":
    main()
