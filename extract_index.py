#!/usr/bin/env python3
"""
Extract index.html source code from a saved GitHub blob page.
Saves result to extract_result.txt in the same directory as this script.

Run with: python3 /path/to/extract_index.py
"""
import re
import sys
import os
import json

# The blob page for index.html (not the repo overview)
FILE = "/var/folders/p6/c875_qrj65n9t18bwfqyq4840000gn/T/claude-hostloop-plugins/599596e2b72964f9/projects/-Users-vl-Library-Application-Support-Claude-local-agent-mode-sessions-bad0d275-62af-462a-9385-cd774f8b1078-126e36b2-a6ac-42e7-a711-4206a8b72f37-local-21859c92-1ca3-4e62-8d3a-38d7bc02ffb7-outputs/ae81cb8c-45b0-4990-9b54-000f667ac655/tool-results/mcp-workspace-web_fetch-1777394126241.txt"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extract_result.txt")

print(f"Reading file...", flush=True)
with open(FILE, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

print(f"File size: {len(content)} chars", flush=True)

results = []
results.append(f"File size: {len(content)} chars\n\n")

# GitHub blob pages embed the file content in a <script> tag with data-target="react-app.embeddedData"
# The JSON has a "payload" key with "blob" -> "rawLines" array

# Find the script tag
match = re.search(
    r'<script type="application/json" data-target="react-app\.embeddedData">(.*?)</script>',
    content,
    re.DOTALL
)

if match:
    print("Found react-app.embeddedData script tag", flush=True)
    json_str = match.group(1)
    print(f"JSON string length: {len(json_str)}", flush=True)
    results.append(f"JSON string length: {len(json_str)}\n\n")

    try:
        data = json.loads(json_str)
        print("JSON parsed successfully", flush=True)

        # Navigate to rawLines
        payload = data.get('payload', {})
        blob = payload.get('blob', {})
        raw_lines = blob.get('rawLines', None)

        if raw_lines is not None:
            print(f"Found rawLines with {len(raw_lines)} lines", flush=True)
            results.append(f"=== index.html SOURCE CODE ({len(raw_lines)} lines) ===\n\n")
            for line in raw_lines:
                results.append(line + "\n")
        else:
            print("rawLines not found in blob, checking other keys...", flush=True)
            # Print structure for debugging
            results.append(f"payload keys: {list(payload.keys())}\n")
            if 'blob' in payload:
                results.append(f"blob keys: {list(payload['blob'].keys())}\n")
                # Try other possible keys
                for key in ['lines', 'fileContents', 'content', 'text']:
                    if key in payload['blob']:
                        results.append(f"\nFound key '{key}':\n")
                        results.append(str(payload['blob'][key])[:10000])
                        results.append("\n")
            # Also check codeViewRoute
            for route_key in ['codeViewBlobRoute', 'codeViewRoute', 'blob']:
                if route_key in payload:
                    results.append(f"\n{route_key} keys: {list(payload[route_key].keys())}\n")
                    blob2 = payload[route_key]
                    if 'rawLines' in blob2:
                        raw_lines2 = blob2['rawLines']
                        results.append(f"\n=== index.html SOURCE CODE via {route_key} ({len(raw_lines2)} lines) ===\n\n")
                        for line in raw_lines2:
                            results.append(line + "\n")
                    elif 'blob' in blob2:
                        results.append(f"\n  blob keys: {list(blob2['blob'].keys())}\n")
                        if 'rawLines' in blob2['blob']:
                            raw_lines3 = blob2['blob']['rawLines']
                            results.append(f"\n=== index.html SOURCE CODE via {route_key}.blob ({len(raw_lines3)} lines) ===\n\n")
                            for line in raw_lines3:
                                results.append(line + "\n")

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", flush=True)
        results.append(f"JSON parse error: {e}\n")
        # Try to find rawLines manually
        rl_idx = json_str.find('"rawLines"')
        if rl_idx != -1:
            results.append(f"rawLines found at pos {rl_idx} in JSON string\n")
            results.append(json_str[rl_idx:rl_idx+100000])
        # Also find VinayPic
        vp_idx = json_str.find('VinayPic')
        if vp_idx != -1:
            results.append(f"\nVinayPic found at pos {vp_idx}\n")
            results.append(json_str[max(0,vp_idx-500):vp_idx+5000])
else:
    print("Script tag not found", flush=True)
    results.append("Script tag NOT found\n")
    # Direct search
    vp_idx = content.find('VinayPic')
    if vp_idx != -1:
        results.append(f"VinayPic at char {vp_idx}\n")
        results.append(content[max(0,vp_idx-1000):vp_idx+20000])

output = "".join(results)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Done. Output written to {OUT} ({len(output)} chars)", flush=True)
