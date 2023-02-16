from dash import Dash
from dash_bootstrap_components.themes import DARKLY

from components import layout


def main() -> None:
    # ticker_data = load_tickers()
    # idx_data = load_indices()
    app = Dash(external_stylesheets=[DARKLY])
    app.title = 'Dashboard'
    # app.layout = layout.create_layout(app, ticker_data, idx_data)
    app.layout = layout.create_layout(app)
    app.run(debug=False)


if __name__ == '__main__':
    main()
