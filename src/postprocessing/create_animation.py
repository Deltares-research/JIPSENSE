"""Create a side-by-side GIF from WH and TR image frames."""

from __future__ import annotations

import argparse
from pathlib import Path

DATA_ROOT = Path(
    "/mnt/p/11212604-jip-sense/DAS/SPECFEM2D_OUTPUTS/"
    "JAPANESE_SOIL_CONDITIONS"
)

# Match direct child directories by their suffixes.
WH_DIRECTORY_SUFFIX = "_wh"
TR_DIRECTORY_SUFFIX = "_tr"

SUPPORTED_IMAGE_SUFFIXES = {".jpg", ".jpeg"}


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Create a side-by-side GIF from WH and TR JPG frames."
    )
    parser.add_argument(
        "--thickness",
        type=float,
        default=1.5,
        help="Sediment thickness in metres (default: %(default)s).",
    )
    parser.add_argument(
        "--results-root",
        type=Path,
        help=(
            "Directory containing the WH and TR output folders. "
            "Defaults to the configured data root for the selected thickness."
        ),
    )
    parser.add_argument(
        "--wh-directory",
        help=(
            "WH frame directory name. Automatically detected by the "
            "_wh suffix if omitted."
        ),
    )
    parser.add_argument(
        "--tr-directory",
        help=(
            "TR frame directory name. Automatically detected by the "
            "_tr suffix if omitted."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output GIF path (default: animation_wh_vs_tr.gif in results root).",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=4,
        help="Animation frame rate (default: %(default)s).",
    )
    return parser.parse_args()


def find_output_directory(
    root: Path, suffix: str, directory_name: str | None
) -> Path:
    """Resolve a frame directory by explicit name or a unique suffix match."""
    if directory_name is not None:
        directory = root / directory_name
        if not directory.is_dir():
            raise FileNotFoundError(f"Frame directory does not exist: {directory}")
        return directory

    matches = (
        sorted(
            path
            for path in root.iterdir()
            if path.is_dir() and path.name.lower().endswith(suffix)
        )
        if root.is_dir()
        else []
    )
    if not matches:
        raise FileNotFoundError(
            f"No frame directory ending in '{suffix}' found in {root}"
        )
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        raise ValueError(
            f"Multiple frame directories ending in '{suffix}' found in {root}: "
            f"{names}. Specify one with the corresponding directory option."
        )
    return matches[0]


def find_frames(directory: Path) -> list[Path]:
    """Return sorted JPG frames from a directory, reporting invalid input."""
    if not directory.is_dir():
        raise FileNotFoundError(f"Frame directory does not exist: {directory}")

    frames = sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_SUFFIXES
    )
    if not frames:
        raise FileNotFoundError(f"No JPG frames found in {directory}")
    return frames


def create_animation(
    wh_frames: list[Path],
    tr_frames: list[Path],
    output_path: Path,
    thickness: float,
    fps: int,
) -> int:
    """Create and save the animation; return the number of frames written."""
    import matplotlib.animation as animation
    import matplotlib.pyplot as plt

    frame_count = min(len(wh_frames), len(tr_frames))

    fig, (wh_axis, tr_axis) = plt.subplots(2, 1, figsize=(10, 6))
    image_artists = []

    for axis, frame_path, label in (
        (wh_axis, wh_frames[0], "WH"),
        (tr_axis, tr_frames[0], "TR"),
    ):
        frame = plt.imread(frame_path)
        frame = frame[: frame.shape[0] // 2, :]
        image_artists.append(axis.imshow(frame))
        axis.axis("off")
        axis.set_title(f"simulation_sediment_on_top_{thickness}m -- {label}")

    def update(frame_index: int) -> tuple:
        for artist, frames in zip(image_artists, (wh_frames, tr_frames)):
            frame = plt.imread(frames[frame_index])
            artist.set_data(frame[: frame.shape[0] // 2, :])
        return tuple(image_artists)

    try:
        movie = animation.FuncAnimation(
            fig, update, frames=frame_count, blit=True
        )
        movie.save(output_path, writer=animation.PillowWriter(fps=fps))
    finally:
        plt.close(fig)

    return frame_count


def main() -> None:
    """Resolve inputs and generate the WH/TR animation."""
    args = parse_args()
    if args.fps <= 0:
        raise ValueError("--fps must be a positive integer.")

    if args.results_root is None:
        if args.thickness == 0.0:
            simulation_directory = "simulation_no_sediment_on_top_JAP"
        else:
            simulation_directory = (
                f"simulation_sediment_on_top_{args.thickness}m_JAP"
            )
        results_root = DATA_ROOT / simulation_directory / "RESULTS"
    else:
        results_root = args.results_root

    wh_directory = find_output_directory(
        results_root, WH_DIRECTORY_SUFFIX, args.wh_directory
    )
    tr_directory = find_output_directory(
        results_root, TR_DIRECTORY_SUFFIX, args.tr_directory
    )
    wh_frames = find_frames(wh_directory)
    tr_frames = find_frames(tr_directory)
    output_path = args.output or results_root / "animation_wh_vs_tr.gif"

    frame_count = create_animation(
        wh_frames,
        tr_frames,
        output_path,
        args.thickness,
        args.fps,
    )
    print(f"Saved {frame_count} frames to {output_path}")


if __name__ == "__main__":
    main()
