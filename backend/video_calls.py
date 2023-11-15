from fastapi import FastAPI,APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/video_call", response_class=HTMLResponse)
async def get_jitsi_page():
    jitsi_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jitsi Meet Integration</title>
        <script src="https://meet.jit.si/external_api.js"></script>
    </head>
    <body>
        <div id="jitsi-container"></div>
        <script>
            const domain = 'meet.jit.si';
            const options = {
                roomName: 'your-room-name',
                width: 800,
                height: 600,
            };
            const api = new JitsiMeetExternalAPI(domain, options);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=jitsi_html)


