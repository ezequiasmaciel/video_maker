import streamlit as st
from modules import image_generator, stock_assets, tts, video_maker


def main():
    st.set_page_config(page_title="AI Video Maker", layout="wide")

    st.title("🎞️ AI Video Maker (100% OSS)")
    st.caption(
        "Gere vídeos a partir de um roteiro usando IA ou clipes gratuitos, com narração humana multilíngue e legendas."
    )

    # Entrada de roteiro
    script_text = st.text_area("Cole seu roteiro (use marcadores CENA 1:, CENA 2:, ...):", height=350)

    # Opções de mídia
    col_media, col_font = st.columns([2, 1])

    with col_media:
        asset_mode = st.radio(
            "Fonte de mídia visual:",
            ["Gerar Imagens com IA", "Vídeos/Imagens de Acervo Gratuito"],
        )

    with col_font:
        font_name = st.selectbox(
            "Fonte da legenda",
            ["DejaVu-Serif", "DejaVu-Sans", "Liberation-Serif", "Liberation-Sans"],
        )

    if st.button("🎬 Gerar Vídeo"):
        if not script_text.strip():
            st.error("Por favor, cole um roteiro primeiro.")
            st.stop()

        # 1. Coletar mídia
        with st.spinner("Coletando/gerando mídia visual …"):
            if asset_mode.startswith("Gerar"):
                media_paths, scenes = image_generator.generate_images(script_text)
            else:
                media_paths = stock_assets.fetch_assets(script_text)
                scenes = image_generator.split_script_into_scenes(script_text)
        st.success(f"{len(media_paths)} cenas prontas.")

        # 2. Narração TTS
        with st.spinner("Gerando narração …"):
            try:
                audio_path = tts.synthesize_speech(script_text)
            except Exception as e:
                st.error(f"Erro ao gerar áudio: {e}")
                st.stop()

        # 3. Compor vídeo com legendas
        with st.spinner("Compondo vídeo final …"):
            video_path = video_maker.compose_video(
                media_paths, audio_path, scenes, font_name, language=None
            )

        st.video(video_path)
        st.success("Vídeo pronto! Faça o download ou publique.")


if __name__ == "__main__":
    main()
