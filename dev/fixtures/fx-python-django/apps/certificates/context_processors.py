"""Custom context processor for the certificates app."""


def certificate_metadata(request):
    return {
        "certificate_authority": "FXDJ Authority",
        "certificate_version": "1.0",
    }