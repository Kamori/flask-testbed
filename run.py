#!/usr/bin/env python3

from src import configure

if __name__ == '__main__':
    server = configure()
    server.run(host='0.0.0.0', port=5000)