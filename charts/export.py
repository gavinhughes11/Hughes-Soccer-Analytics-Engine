from io import BytesIO


def to_png(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=200, bbox_inches="tight")
    return buffer.getvalue()
