import machine
import network
import socket


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)

    return connection


def webpage(temperature, client_id):
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            <p>Pico: {client_id}</p>
            <p>Temperatura: {temperature}</p>
            </body>
            </html>
            """
    return str(html)


def serve(ip, client_id, temperature):
    # Start a web server
    while True:
        connection = open_socket(ip)
        client = connection.accept()[0]
        html = webpage(temperature, client_id)
        client.send(html)
        client.close()

