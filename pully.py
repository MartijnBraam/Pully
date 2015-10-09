#!/usr/bin/env python2
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import argparse
import subprocess

args = None


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        gitlab_hook_type = self.headers.getheader('X-Gitlab-Event')
        if gitlab_hook_type is None:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("This is not a Gitlab webhook event")
            print("Request is not a Gitlab webhook. It doesn't contain the X-Gitlab-Event header.")
            return

        remote_addr = self.client_address[0]

        if remote_addr != args.source:
            self.send_response(403)
            self.end_headers()
            self.wfile.write("Gitlab events not allowed from this IP")
            print("Gitlab events not allowed from {}.".format(remote_addr))
            return

        print("Received hook: {} from {}".format(gitlab_hook_type, remote_addr))

        if gitlab_hook_type == "Push Hook":
            if args.exec_push == "":
                print("No command defined for push events (--exec-push)")
            else:
                subprocess.call(args.exec_push, shell=True)
        elif gitlab_hook_type == "Tag Push Hook":
            if args.exec_tag == "":
                print("No command defined for push events (--exec-tag)")
            else:
                subprocess.call(args.exec_tag, shell=True)

        message = 'ok'
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pully Gitlab webhook receiver")
    parser.add_argument("--port", "-p", help="Port to listen on", type=int, default=30123)
    parser.add_argument("--source", "-s", help="Source IP of the Gitlab webhooks", type=str, default="127.0.0.1")
    parser.add_argument("--exec-push", help="Command to execute when commits are pushed to the repository", type=str,
                        default="")
    parser.add_argument("--exec-tag", help="Command to execute when tags are pushed to the repository", type=str,
                        default="")
    args = parser.parse_args()

    server = HTTPServer(('0.0.0.0', args.port), RequestHandler)
    print 'Starting server on port {}, use <Ctrl-C> to stop'.format(args.port)
    print 'Allowing webhooks from {}'.format(args.source)
    server.serve_forever()
