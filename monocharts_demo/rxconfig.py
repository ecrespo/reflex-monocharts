import reflex as rx
from reflex.plugins import RadixThemesPlugin, SitemapPlugin

config = rx.Config(
    app_name="monocharts_demo",
    plugins=[
        RadixThemesPlugin(
            theme=rx.theme(appearance="dark", accent_color="gray", radius="large"),
        ),
        SitemapPlugin(),
    ],
)
