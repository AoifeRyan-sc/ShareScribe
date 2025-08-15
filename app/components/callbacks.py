from dash import dcc, callback, Input, Output, State, html, no_update
from utils import parse_contents, check_file, srt_to_docx, translate_transcription
from dash.exceptions import PreventUpdate

def register_all_callbacks(app):
    @app.callback(
            Output('file-error-message', 'displayed'),
            Output('file-error-message', 'message'),
            Output('upload-data', 'contents'),
            Output('upload-data', 'filename'),
            Output('lang-error-message', 'displayed'),
            Output('lang-error-message', 'message'),
            Input('upload-data', 'contents'),
            Input('go-button', 'n_clicks'),
            State('upload-data', 'filename'),
            State('action-input', 'value'),
            State('translate-from-dropdown', 'value'),
            State('translate-to-dropdown', 'value'),
            prevent_initial_call=True
            )
    def file_check_callback(content, nclicks, name, activity, translate_to, translate_from):
        print("nclicks: ", nclicks)

        if content is None and nclicks > 0:
            print("checking file upload")
            return True, f'No file uploaded', None, None, None, None
    
        if content is not None and activity == "translations":
            print(translate_from)
            print(translate_to)
            print("file check callback")
            check_output = check_file(content, name)

            if type(check_output) == str:
                return True, check_output, None, None

        return False, None, content, name

    @app.callback(
            Output("processed_file", "data"),
            Output('api_output_text', 'children'),
            Input('go-button', 'n_clicks'),
            State('action-input', 'value'),
            State('transcribe-from-dropdown', 'value'),
            State('translate-from-dropdown', 'value'),
            State('translate-to-dropdown', 'value'),
            State('no-translate-words', 'value'),
            State('upload-data', 'contents'),
            State('upload-data', 'filename'),
            prevent_initial_call=True
            )
    def update_output(n_clicks, action, transcribe_lang, translate_from, translate_to, no_translate_words, content, filename):

        if content is not None and n_clicks > 0:

            if action == "translations" and translate_to != "en":
                print(translate_from)
                print(translate_to)

                parsed_file =  parse_contents(action = "transcriptions", contents = content, transcribe_language = translate_from)
                processed_file = translate_transcription(parsed_file, language_to=translate_to, language_from=translate_from, words = no_translate_words)

            else:
                print(transcribe_lang)
                lang = transcribe_lang if action == "transcriptions" else None
                processed_file =  parse_contents(action, content, transcribe_language = lang)


            processed_dict = {"processed_file": processed_file,
                              "processed_file_name": filename}

            return processed_dict, processed_file
            
        return None, None

    @app.callback(
        Output("upload-status", "children"),
        Input("upload-data", "contents"),
        Input("processed_file", "data"),
        State("upload-data", "filename"),
        prevent_initial_call=True
    )
    def show_upload_progress(contents, file_state, filename):

        if file_state is not None:
            processed_file_name = file_state["processed_file_name"]
            print(processed_file_name)

            if filename == processed_file_name:
                return f"Processed file: {filename}, press Download button to save"

            elif filename != processed_file_name:
                return f"Uploaded file: {filename}"
            
        elif contents is None:
            raise PreventUpdate
        
        return f"Uploaded file: {filename}"

    @app.callback(
        Output("download-transcript", "data"),
        Input("download-button", "n_clicks"),
        State('output-type', 'value'),
        State("processed_file", "data"),
        State("upload-data", "filename"),    
    )
    def download_file(n_clicks, response_format, processed_data, filename):
        print("download triggered")
        if n_clicks > 0:
            print("nclicks > 0")
            processed_data = processed_data["processed_file"]
            file_name = filename.split('.')[0].lower()
            download_title = "".join([file_name,".", response_format])
            print(download_title)

            if response_format == "docx":
                byte_stream = srt_to_docx(processed_data)
                
                return dcc.send_bytes(
                    byte_stream.getvalue(),
                    download_title
                )
            
            return dict(content=processed_data, filename=download_title)


    @app.callback(
        # Output('download-button', 'style'),
        Output("display-col", "style"),
        Input('processed_file', 'data'),
        Input('upload-data', 'filename')
    )
    def show_download_button(processed_file, filename):
        
        if processed_file is not None:
            # processed_file_name = processed_file["processed_file_name"]
            # if processed_file_name == filename:
            return {'display': 'inline-block'}
    
        return {'display': 'none'}
        # return {'display': 'inline-block'}

    @app.callback(
        Output("select-translation-language", "style"),
        Output("select-transcription-language", "style"),
        Output("word-exclusions", "style"),
        Input("action-input", "value")
    )
    def show_language_select(api_action):
        
        no_display_dropdown_style = {'display': "none"}
        display_dropdown_style = {
                'width': '100%', 
                'display': 'flex',
                'fontSize': '16px', 
                'paddingTop': '10px',
                'gap': '10px'
                }
        text_input_style = {'display': "none"}
        
        if api_action == "translations":
            translation_dropdown_style = display_dropdown_style
            text_input_style = {'display': 'inline-block', 'width': '100%', 'paddingTop': '10px',}
            transcription_dropdown_style = no_display_dropdown_style

            return translation_dropdown_style, transcription_dropdown_style, text_input_style
        
        return no_display_dropdown_style, display_dropdown_style, text_input_style


    @app.callback(
        Output('spinner-fast-trigger', 'children'), # This is the output the spinner will "see" activate first
        Input('go-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def trigger_spinner_immediately(n_clicks):
        if n_clicks is None:
            raise no_update
        return ""
