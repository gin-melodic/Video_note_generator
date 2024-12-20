import gradio as gr
from gradio_modal import Modal

from src.logger import app_logger

# Initialize global settings
global_setting = {
    "openrouter_api_key": '',
    "openrouter_api_url": 'https://openrouter.ai/api/v1',
    "openrouter_app_name": 'rednote-generator',
    "openrouter_http_referer": 'https://github.com',
    "unsplash_access_key": '',
    "unsplash_secret_key": '',
    "unsplash_redirect_uri": 'https://github.com',
    "whisper_model": 'medium',
    "whisper_language": 'zh',
    "ffmpeg_path": '',
    "http_proxy": '',
    "https_proxy": '',
    "output_dir": 'generated_notes',
    "max_tokens": 5000,
    "content_chunk_size": 2000,
    "temperature": 0.7,
    "top_p": 0.9,
    "use_emoji": True,
    "tag_count": 5,
    "min_paragraphs": 3,
    "max_paragraphs": 6,
    "debug": False,
    "log_level": 'info'
}


def update_input_visibility(choice):
    return (
        gr.update(visible=(choice == "单URL")),
        gr.update(visible=(choice == "多行URL文档")),
        gr.update(visible=(choice == "MD文档"))
    )

def main():
    with gr.Blocks(title='爆款生成器') as demo:
        # Create a State to hold global settings
        settings_state = gr.State(value=global_setting)

        gr.Markdown("# 操作区")

        # Main interface components
        with gr.Row():
            model_name = gr.Textbox(label="Openrouter模型名", value="google/gemini-2.0-flash-exp:free",
                                    interactive=True)
            parse_type = gr.Radio(
                label="解析内容",
                choices=["单URL", "多行URL文档", "MD文档"],
                value="单URL"
            )

        # Input Components
        with gr.Group():
            url_input = gr.Textbox(label="url 名称", visible=True, interactive=True)
            file_input = gr.File(label="上传文档", visible=False, interactive=True, type='binary')
            md_file_input = gr.File(label="上传文档", visible=False, interactive=True, type='binary')

        parse_type.change(
            fn=update_input_visibility,
            inputs=[parse_type],
            outputs=[url_input, file_input, md_file_input]
        )

        # Buttons for actions
        with gr.Row():
            settings_btn = gr.Button("设置")
            generate_btn = gr.Button("生成")

        # Tabs for results
        with gr.Tabs(visible=False):
            with gr.TabItem("转录文档"):
                transcript_output = gr.Markdown()
                copy_transcript_button = gr.Button("复制")

            with gr.TabItem("整理文档"):
                organized_output = gr.Markdown()
                copy_organized_button = gr.Button("复制")

            with gr.TabItem("小红书文档"):
                xiaohongshu_output = gr.Markdown()
                download_image_button = gr.Button("下载图片")
                copy_xiaohongshu_button = gr.Button("复制")

        # Settings Modal
        def update_global_settings(*args):
            keys = list(global_setting.keys())
            return {key: value for key, value in zip(keys, args)}

        def load_settings(settings):
            return [settings[key] for key in global_setting.keys()]

        with Modal(visible=False) as settings_modal:
            gr.Markdown("# 设置")

            # Settings Tabs
            with gr.Tabs():
                # OpenRouter Settings
                with gr.TabItem("OpenRouter设置"):
                    openrouter_api_key = gr.Textbox(label="OPENROUTER_API_KEY", interactive=True, placeholder="Require, Fill your API key here")
                    openrouter_api_url = gr.Textbox(label="OPENROUTER_API_URL", interactive=True, placeholder="Require, OpenRouter API URL")
                    openrouter_app_name = gr.Textbox(label="OPENROUTER_APP_NAME", interactive=True, placeholder="Require, OpenRouter App Name")
                    openrouter_http_referer = gr.Textbox(label="OPENROUTER_HTTP_REFERER", interactive=True, placeholder="Require, OpenRouter HTTP Referer")

                # Unsplash Settings
                with gr.TabItem("Unsplash设置"):
                    unsplash_access_key = gr.Textbox(label="UNSPLASH_ACCESS_KEY", interactive=True, placeholder="Unsplash Access Key")
                    unsplash_secret_key = gr.Textbox(label="UNSPLASH_SECRET_KEY", interactive=True, placeholder="Unsplash Secret Key")
                    unsplash_redirect_uri = gr.Textbox(label="UNSPLASH_REDIRECT_URI", interactive=True, placeholder="Unsplash Redirect URI")

                # Whisper Settings
                with gr.TabItem("Whisper设置"):
                    whisper_model = gr.Radio(
                        label="WHISPER_MODEL",
                        choices=["tiny", "base", "small", "medium", "large-v2"], interactive=True
                    )
                    whisper_language = gr.Radio(
                        label="WHISPER_LANGUAGE",
                        choices=["zh", "en", "ja"], interactive=True
                    )
                    ffmpeg_path = gr.Textbox(label="FFMPEG_PATH", interactive=True, placeholder="Windows 用户需要设置 FFmpeg 路径，Mac/Linux 用户通常不需要")

                # Proxy Settings
                with gr.TabItem("代理设置"):
                    http_proxy = gr.Textbox(label="HTTP_PROXY", interactive=True)
                    https_proxy = gr.Textbox(label="HTTPS_PROXY", interactive=True)

                # Generation Settings
                with gr.TabItem("生成设置"):
                    output_dir = gr.Textbox(label="OUTPUT_DIR", interactive=True, placeholder="Output Directory")
                    max_tokens = gr.Slider(label="MAX_TOKENS", minimum=100, maximum=5000, step=100, interactive=True, info='生成小红书内容的最大长度')
                    content_chunk_size = gr.Slider(label="CONTENT_CHUNK_SIZE", minimum=100, maximum=5000, step=100, interactive=True, info='长文本分块大小（字符数）')
                    temperature = gr.Slider(label="TEMPERATURE", minimum=0.0, maximum=1.0, step=0.1, interactive=True, info='AI 创造性程度 (0.0-1.0)')
                    top_p = gr.Slider(label="TOP_P", minimum=0.0, maximum=1.0, step=0.1, interactive=True, info='采样阈值 (0.0-1.0)')
                    use_emoji = gr.Checkbox(label="USE_EMOJI", interactive=True, info='是否在内容中使用表情符号')
                    tag_count = gr.Slider(label="TAG_COUNT", minimum=1, maximum=10, step=1, interactive=True, info='生成的标签数量')
                    min_paragraphs = gr.Slider(label="MIN_PARAGRAPHS", minimum=1, maximum=10, step=1, interactive=True, info='最少段落数')
                    max_paragraphs = gr.Slider(label="MAX_PARAGRAPHS", minimum=1, maximum=10, step=1, interactive=True, info='最多段落数')

                # Debug Settings
                with gr.TabItem("调试设置"):
                    debug = gr.Checkbox(label="DEBUG", interactive=True)
                    log_level = gr.Radio(
                        label="LOG_LEVEL",
                        choices=["debug", "info", "warning", "error"], interactive=True
                    )

            confirm_btn = gr.Button("确认")

        settings_btn.click(lambda: Modal(visible=True), None, settings_modal)
        # Load settings into modal on button click
        settings_btn.click(
            fn=load_settings,
            inputs=[settings_state],
            outputs=[
                openrouter_api_key, openrouter_api_url, openrouter_app_name,
                openrouter_http_referer, unsplash_access_key, unsplash_secret_key,
                unsplash_redirect_uri, whisper_model, whisper_language,
                ffmpeg_path, http_proxy, https_proxy, output_dir,
                max_tokens, content_chunk_size, temperature,
                top_p, use_emoji, tag_count,
                min_paragraphs, max_paragraphs, debug,
                log_level
            ]
        )

        # Update global settings on confirm button click
        confirm_btn.click(
            fn=update_global_settings,
            inputs=[
                openrouter_api_key, openrouter_api_url, openrouter_app_name,
                openrouter_http_referer, unsplash_access_key, unsplash_secret_key,
                unsplash_redirect_uri, whisper_model, whisper_language,
                ffmpeg_path, http_proxy, https_proxy, output_dir,
                max_tokens, content_chunk_size, temperature,
                top_p, use_emoji, tag_count,
                min_paragraphs, max_paragraphs, debug,
                log_level
            ],
            outputs=[settings_state]
        )
        confirm_btn.click(lambda: Modal(visible=False), None, settings_modal)

    demo.launch()


if __name__ == "__main__":
    main()
