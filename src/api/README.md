# Test the Simulon API

## 1. Start the FastAPI Server

From your project root directory, run:
```bash
uvicorn src.api.main:app --reload
```

**Server Information:**
- API Server: http://127.0.0.1:8000
- Interactive API Docs: http://127.0.0.1:8000/docs
- Alternative Docs: http://127.0.0.1:8000/redoc

## 2. Test the API Endpoints

### Step 1: Open the API Documentation
1. Navigate to: http://127.0.0.1:8000/docs
2. You'll see the Swagger UI with all available endpoints

### Step 2: Test the Numerical Solver
1. **Find the `/solve/numerical` endpoint** (POST method)
2. **Click "Try it out"**
3. **Copy and paste this JSON into the request body:**
```json
{
  "length": 1.0,
  "nx": 10,
  "alpha": 0.01,
  "dt": 0.001,
  "t_final": 0.01,
  "u0": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "bc_left": 1.0,
  "bc_right": 0.0,
  "save_every": 1
}
```

4. **Click "Execute"**
5. **Copy the `simulation_id` from the response** (you'll need this for visualization)

**Expected Response:**
```json
{
  "simulation_id": "some-uuid-here",
  "solution_shape": [11, 10]
}
```

### Step 3: Visualize the Simulation
1. **Find the `/visualize/{sim_id}` endpoint** (GET method)
2. **Click "Try it out"**
3. **Paste ONLY the simulation_id** into the `sim_id` field
4. **Click "Execute"**
5. **Download the GIF file** that appears in the response

## 3. Parameter Explanation

| Parameter | Description | Example Value |
|-----------|-------------|---------------|
| `length` | Length of the 1D domain | 1.0 |
| `nx` | Number of spatial grid points | 10 |
| `alpha` | Diffusion coefficient | 0.01 |
| `dt` | Time step size | 0.001 |
| `t_final` | Final simulation time | 0.01 |
| `u0` | Initial condition (array of nx values) | [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] |
| `bc_left` | Left boundary condition | 1.0 |
| `bc_right` | Right boundary condition | 0.0 |
| `save_every` | Save solution every N time steps | 1 |

## 4. Troubleshooting

### Common Issues:
- **404 "Simulation not found"**: Make sure you're using the correct simulation_id and haven't restarted the server
- **500 Internal Server Error**: Check that the `tmp/` directory exists in your project root
- **Import errors**: Ensure your virtual environment is activated and dependencies are installed

### If the server won't start:
```bash
# Check if port 8000 is available
netstat -an | findstr :8000

# Use a different port if needed
uvicorn src.api.main:app --reload --port 8001
```