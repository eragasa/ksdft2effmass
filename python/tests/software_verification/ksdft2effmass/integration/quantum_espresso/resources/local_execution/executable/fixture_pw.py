#!/usr/bin/env python3
"""Deterministic process fixture; no scientific calculation is performed."""

import os
import signal
import sys
import time

mode = sys.argv[1] if len(sys.argv) > 1 else "--fixture-mode"

if mode == "--fixture-timeout":
    sys.stdout.write("FIXTURE ENTERED\n")
    sys.stdout.flush()
    time.sleep(10.0)
elif mode == "--fixture-signal":
    sys.stdout.write("FIXTURE ENTERED\n")
    sys.stdout.flush()
    os.kill(os.getpid(), signal.SIGTERM)
elif mode == "--fixture-fail":
    sys.stdout.write("FIXTURE PROCESS FAILURE\n")
    sys.stderr.write("FIXTURE STDERR\n")
    raise SystemExit(3)
elif mode == "--fixture-calculator-fail":
    sys.stdout.write("DIAGNOSTIC: FATAL c_bands too many bands are not converged\n")
    raise SystemExit(1)
elif mode == "--fixture-after-snapshot-fail":
    os.symlink("missing", "results/unsupported-link")
    sys.stdout.write("JOB DONE.\n")
elif mode == "--fixture-output-limit":
    sys.stdout.buffer.write(b"x" * 65_536)
    sys.stdout.flush()
    time.sleep(10.0)
elif mode == "--fixture-empty-stderr":
    sys.stdout.write("JOB DONE.\n")
elif mode == "--fixture-echo-stdin":
    sys.stdout.buffer.write(sys.stdin.buffer.read())
elif mode == "--fixture-mode":
    sys.stdout.write("JOB DONE.\n")
    sys.stderr.write("DIAGNOSTIC: NONBLOCKING synthetic floating-point notice\n")
else:
    sys.stderr.write("UNKNOWN FIXTURE MODE\n")
    raise SystemExit(64)
