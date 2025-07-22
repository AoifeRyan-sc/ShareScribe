from dash import callback, Input, Output, State
from utils import parse_contents, check_file, srt_to_docx
from dash.exceptions import PreventUpdate

def register_all_callbacks(app):
    @app.callback(
            Output('error-message', 'displayed'),
            Output('error-message', 'message'),
            Output('upload-data', 'contents'),
            Output('upload-data', 'filename'),
            Input('upload-data', 'contents'),
            Input('go-button', 'n_clicks'),
            State('upload-data', 'filename'),
            prevent_initial_call=True
            )
    def file_check_callback(content, nclicks, name):
        print("nclicks: ", nclicks)

        if content is None and nclicks > 0:
            print("checking file upload")
            return True, f'No file uploaded', None, None
    
        if content is not None:
            print("file check callback")
            check_output = check_file(content, name)

            if type(check_output) == str:
                return True, check_output, None, None

        return False, None, content, name

    @app.callback(
            Output("processed_file", "data"),
            Output('processing-complete-modal', 'is_open'),
            Output('modal_message', 'children'),
            Input('go-button', 'n_clicks'),
            State('action-input', 'value'),
            State('output-type', 'value'),
            State('upload-data', 'contents'),
            State('upload-data', 'filename'),
            prevent_initial_call=True
            )
    def update_output(n_clicks, action, response_format, content, filename):

        if content is not None and n_clicks > 0:
            
            processed_file =  parse_contents(action, content, response_format)
            processed_dict = {"processed_file": processed_file,
                            "processed_file_name": filename}

            return processed_dict, True, processed_file 
        return None, False, None

    @app.callback(
        Output("loading-output", "children"),
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
                return None, f"Processed file: {filename}, press Download button to save"

            elif filename != processed_file_name:
                return None, f"Uploaded file: {filename}"
            
        elif contents is None:
            raise PreventUpdate
        
        return None, f"Uploaded file: {filename}"

    @app.callback(
        Output("download-transcript", "data"),
        Input("download-button", "n_clicks"),
        State('output-type', 'value'),
        State("processed_file", "data"),
        State("upload-data", "filename"),    
    )
    def download_file(n_clicks, response_format, processed_data, filename):
        if n_clicks > 0:
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
        Output('download-button', 'style'),
        Input('processed_file', 'data'),
        Input('upload-data', 'filename')
    )
    def show_download_button(processed_file, filename):
        
        if processed_file is not None:
            processed_file_name = processed_file["processed_file_name"]
            if processed_file_name == filename:
                return {'display': 'inline-block'}  # Make button visible
    
        return {'display': 'none'} 

