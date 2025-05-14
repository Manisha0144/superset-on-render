from fastapi import FastAPI, HTTPException
import subprocess
import os
 
app = FastAPI()
 
@app.post("/run-script")
async def run_script(data: dict):
    result = subprocess.run(
        ['python3', 'superset_fetcher.py',
         data['base_url'], data['username'],
         data['password'], str(data['chart_id'])],
        capture_output=True, text=True
    )
    return {
        "status": "success",
        "output": result.stdout,
        "error": result.stderr
    }
