"""Assert that the installer rejects native Windows junction boundaries."""

import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile


def _create_junction(link: Path, target: Path) -> None:
    subprocess.run(
        ["cmd.exe", "/c", "mklink", "/J", str(link), str(target)],
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if not link.is_junction():
        raise RuntimeError("Windows did not create the expected junction: %s" % link)
    if link.is_symlink():
        raise RuntimeError("junction fixture was also classified as a symlink: %s" % link)


def _expect_rejected(label, operation) -> None:
    try:
        operation()
    except installer.InstallerError as error:
        print("%s: rejected (%s)" % (label, error))
    else:
        raise AssertionError("%s: junction was accepted" % label)


if os.name != "nt":
    raise SystemExit("T-017 junction probe requires native Windows")
if sys.version_info < (3, 12):
    raise SystemExit("T-017 junction probe requires Python 3.12 or newer")

sys.path.insert(0, str(Path.cwd() / "scripts"))
import installer  # noqa: E402


with tempfile.TemporaryDirectory(prefix="t017-junction-") as temporary:
    base = Path(temporary)
    install_target = base / "outside-install-target"
    install_target.mkdir()
    member_target = base / "outside-member-target"
    member_target.mkdir()
    (member_target / "leaf.txt").write_text("outside", encoding="utf-8")

    output_target = base / "outside-output-target"
    output_target.mkdir()

    install_junction = base / "install-junction"
    member_junction = base / "member-junction"
    output_junction = base / "output-junction"
    junctions = (install_junction, member_junction, output_junction)

    try:
        _create_junction(install_junction, install_target)
        _create_junction(member_junction, member_target)
        _create_junction(output_junction, output_target)
        before_member = (member_target / "leaf.txt").read_bytes()
        before_output = tuple(sorted(path.name for path in output_target.iterdir()))

        print(
            "fixture: symlink=%s junction=%s"
            % (member_junction.is_symlink(), member_junction.is_junction())
        )
        _expect_rejected(
            "install root",
            lambda: installer._resolve_target_root(install_junction),
        )
        _expect_rejected(
            "adopt root",
            lambda: installer._validated_adoption_root(member_junction),
        )
        _expect_rejected(
            "export output",
            lambda: installer._validated_export_output(output_junction),
        )
        member_state = installer._adoption_target(
            base, PurePosixPath("member-junction/leaf.txt"), {}
        )
        if member_state != ("parent-junction", None):
            raise AssertionError("adopt member through junction: %r" % (member_state,))
        print("adopt member through junction: blocked")

        after_member = (member_target / "leaf.txt").read_bytes()
        after_output = tuple(sorted(path.name for path in output_target.iterdir()))
        if tuple(install_target.iterdir()) or before_member != after_member or before_output != after_output:
            raise RuntimeError("junction probe unexpectedly modified an outside target")
        print("outside targets unchanged: true")
    finally:
        for link in junctions:
            if os.path.lexists(link):
                os.rmdir(link)
