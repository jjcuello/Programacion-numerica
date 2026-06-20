import json
import threading
import unittest
from urllib import request

from src.interfaces.web.app import create_server


class WebApiTests(unittest.TestCase):
    def test_solve_endpoint_runs_newton(self):
        server = create_server(host="127.0.0.1", port=0)
        try:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            url = f"http://127.0.0.1:{server.server_port}/api/roots/solve"
            payload = json.dumps(
                {
                    "method": "newton",
                    "expression": "x**3 - x - 2",
                    "x0": 1.5,
                    "tolerance": 1e-6,
                    "max_iterations": 50,
                }
            ).encode("utf-8")
            response = request.urlopen(
                request.Request(
                    url,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
            )

            body = json.loads(response.read().decode("utf-8"))
            payload = body["result"]
            self.assertEqual(payload["status"], "success")
            self.assertAlmostEqual(payload["root"], 1.52138, places=4)
            self.assertGreater(len(payload["iterations"]), 0)
        finally:
            server.shutdown()
            server.server_close()

    def test_compare_endpoint_runs_all_root_methods(self):
        server = create_server(host="127.0.0.1", port=0)
        try:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            url = f"http://127.0.0.1:{server.server_port}/api/roots/compare"
            payload = json.dumps(
                {
                    "methods": ["bisection", "secant", "newton", "fixedpoint"],
                    "expression": "x**3 - x - 2",
                    "interval": [1.0, 2.0],
                    "x0": 1.5,
                    "g_expression": "(x + 2)**(1/3)",
                    "tolerance": 1e-6,
                    "max_iterations": 100,
                }
            ).encode("utf-8")
            response = request.urlopen(
                request.Request(
                    url,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
            )

            body = json.loads(response.read().decode("utf-8"))
            self.assertEqual(set(body["results"].keys()), {"bisection", "secant", "newton", "fixedpoint"})
            self.assertEqual(body["results"]["bisection"]["status"], "success")
            self.assertEqual(body["results"]["secant"]["status"], "success")
            self.assertEqual(body["results"]["newton"]["status"], "success")
            self.assertEqual(body["results"]["fixedpoint"]["status"], "success")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()