from dash import dcc, html

# Styling
TAB_SELECTED_BG_COLORS = {
    'style': '#fca311',
    'selected_style': '#fcbf49',
}
TAB_CONTENT_STYLES = {
    name: {
        'margin': '0',
        'padding': '0.5rem',
        'width': '80%',
        'aspect-ratio': 'square',
        'background-color': TAB_SELECTED_BG_COLORS[name],
        'border-radius': '0.25rem',
        'border': '0',
        'font-weight': '900',
    } for name in ['style', 'selected_style']
}


def create_tabs(tab_contents):
    return (
        dcc.Tabs(
            children=[
                dcc.Tab(
                    label=tab_content['label'],
                    children=[
                        html.Div(
                            children=tab_content['content'],
                            className="h-screen w-full p-4 flex flex-col"
                            if 'override_className' not in tab_content
                            else tab_content['override_className']
                        )
                    ],
                    style=TAB_CONTENT_STYLES['style'],
                    selected_style=TAB_CONTENT_STYLES['selected_style'],
                ) for tab_content in tab_contents
            ],
            style={
                'width': '4rem',
                'height': '100vh',
                'padding': '1rem 0 0 0',
                'margin': '0',
                'top': '0',
                'left': '0',
                'display': 'flex',
                'flex-direction': 'column',
                'background-color': '#fca311',
                'align-items': 'center',
                'gap': '1rem'
            },
            parent_style={
                'width': '100%',
                'display': 'flex',
                'flexDirection': 'row'
            },
        )
    )
