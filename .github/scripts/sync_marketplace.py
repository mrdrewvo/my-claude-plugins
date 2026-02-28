#!/usr/bin/env python3
import json, re, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def git(*args):
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def changed_files():
    try:
        return git("diff", "--name-only", "HEAD~1", "HEAD").splitlines()
    except subprocess.CalledProcessError:
        return git("diff", "--name-only", "--root", "HEAD").splitlines()


def detect_changed_plugins(files):
    plugins = set()
    for f in files:
        parts = Path(f).parts
        if len(parts) < 2:
            continue
        name = parts[0]
        if name.startswith(".") or name == ".github":
            continue
        if "versions" in parts:
            continue
        candidate = ROOT / name
        if (candidate / ".claude-plugin" / "plugin.json").exists():
            plugins.add(name)
    return plugins


def get_bump_kind(commit_msg):
    first_line = commit_msg.split("\n")[0]
    if "BREAKING CHANGE" in commit_msg or re.search(r"\w+!:", first_line):
        return "major"
    if re.match(r"feat(\(.*?\))?:", first_line):
        return "minor"
    return "patch"


def bump_version(version, kind):
    major, minor, patch = map(int, version.split("."))
    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def create_snapshot(plugin_dir: Path, version: str):
    dest = plugin_dir / "versions" / version
    if dest.exists():
        return
    dest.mkdir(parents=True)
    for item in plugin_dir.iterdir():
        if item.name == "versions":
            continue
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def update_plugin_json(plugin_dir: Path, new_version: str):
    pj = plugin_dir / ".claude-plugin" / "plugin.json"
    data = json.loads(pj.read_text())
    data["version"] = new_version
    pj.write_text(json.dumps(data, indent=2) + "\n")


def update_marketplace_json(plugin_name: str, new_version: str):
    mp = ROOT / ".claude-plugin" / "marketplace.json"
    data = json.loads(mp.read_text())
    for plugin in data["plugins"]:
        if plugin["name"] == plugin_name:
            plugin["version"] = new_version
            break
    mp.write_text(json.dumps(data, indent=2) + "\n")


def update_readme(plugin_name: str, old_version: str, new_version: str):
    readme = ROOT / "README.md"
    text = readme.read_text()
    updated = re.sub(
        rf"(\|\s*\[{re.escape(plugin_name)}\][^|]+\|\s*){re.escape(old_version)}(\s*\|)",
        rf"\g<1>{new_version}\g<2>",
        text,
    )
    readme.write_text(updated)


def main():
    commit_msg = git("log", "-1", "--pretty=%B")
    if "[skip ci]" in commit_msg or commit_msg.strip().startswith("chore: sync marketplace"):
        print("Sync commit detected — skipping.")
        return

    files = changed_files()
    changed_plugins = detect_changed_plugins(files)

    if not changed_plugins:
        print("No plugin source files changed.")
        return

    bump_kind = get_bump_kind(commit_msg)
    print(f"Bump kind: {bump_kind}")

    for plugin_name in sorted(changed_plugins):
        plugin_dir = ROOT / plugin_name
        pj = plugin_dir / ".claude-plugin" / "plugin.json"
        old_version = json.loads(pj.read_text())["version"]
        new_version = bump_version(old_version, bump_kind)
        print(f"{plugin_name}: {old_version} → {new_version}")
        create_snapshot(plugin_dir, new_version)
        update_plugin_json(plugin_dir, new_version)
        update_marketplace_json(plugin_name, new_version)
        update_readme(plugin_name, old_version, new_version)


if __name__ == "__main__":
    main()
