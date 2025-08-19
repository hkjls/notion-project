import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.asgi:application",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="./key.pem",     # votre clé privée
        ssl_certfile="./cert.pem",    # votre certificat
        reload=True                   # optionnel, pour le développement
    )
