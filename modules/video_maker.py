"""Composição de vídeo com legendas (burn‑in) e Ken Burns."""
from typing import List
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip,
    TextClip,
    vfx,
)
from pathlib import Path
import tempfile


def compose_video(
    media_paths: List[str],
    audio_path: str,
    scenes: List[str],
    font_name: str,
    lang: str,
) -> str:
    clips = []
    duration_per_scene = 4  # s

    for path, subtitle in zip(media_paths, scenes):
        img_clip = (
            ImageClip(path)
            .set_duration(duration_per_scene)
            .resize(width=1080)
            .fx(vfx.scroll, w=1080, h=1920, x_speed=5, y_speed=0)
        )
        text_clip = (
            TextClip(
                subtitle,
                fontsize=48,
                font=font_name,
                bg_color="transparent",
                color="white",
                stroke_color="black",
                stroke_width=1,
            )
            .set_position(("center", "bottom"))
            .set_duration(duration_per_scene)
        )
        comp = CompositeVideoClip([img_clip, text_clip])
        clips.append(comp)

    video = concatenate_videoclips(clips, method="compose")
    narration = AudioFileClip(audio_path)
    video = video.set_audio(narration)

    out_path = Path(tempfile.mkstemp(suffix=".mp4")[1])
    video.write_videofile(
        out_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
    )
    return str(out_path)
