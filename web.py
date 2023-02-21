from quart import Quart

app = Quart("ready2scanlate-rest")

@app.get("/")
async def root():
    return { "message": "server working!!" }

if __name__ == "__main__":
    app.run()